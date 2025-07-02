import os
import uuid
import configparser
from datetime import datetime, timedelta
import subprocess
from urllib.parse import urlparse

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

def failure_callback(context):
    dag_run = context.get("dag_run")
    task_instance = context.get("task_instance")
    print(f"[ALERT] Task {task_instance.task_id} in DAG {dag_run.dag_id} failed.")

def generate_timestamped_batch_name(base_name):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}-{ts}"

def log_trigger_info(**context):
    dag_run = context.get("dag_run")
    if dag_run:
        print(f"[INFO] Triggered by DAG ID: {dag_run.external_trigger}")
        print(f"[INFO] Run ID: {dag_run.run_id}")
        print(f"[INFO] Execution Date: {dag_run.execution_date}")
    else:
        print("[INFO] DAG run context is missing.")


def parse_gcs_path(gcs_uri):
    if not gcs_uri.startswith("gs://"):
        raise ValueError("Invalid GCS URI")

    parsed = urlparse(gcs_uri)
    bucket = parsed.netloc
    prefix = parsed.path.lstrip("/")

    return prefix

log_trigger_metadata = PythonOperator(
    task_id="log_trigger_metadata",
    python_callable=log_trigger_info,
    provide_context=True
)

# ----------------------
# Load Config
# ----------------------
ENV = os.getenv("CAEC_ENV", "dev")
CONFIG_PATH = f"/usr/app/src/main/resources/etc/{ENV}.properties"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

PROJECT_ID = config.get("COMMON", "project_id")
REGION = config.get("COMMON", "region")
BUCKET = config.get("COMMON", "bucket")
SERVICE_ACCOUNT = config.get("COMMON", "sa_de_email")


SESSIONIZED_EVENTS_PATH = config.get("PATHS", "sessionized_events")
BASE_PREFIX = parse_gcs_path(SESSIONIZED_EVENTS_PATH)

BQ_DATASET = config.get("BQ", "dataset_staging")
BQ_TABLE = config.get("BQ", "table_sessionized")
BQ_TABLE_PARTITION_FIELD = config.get("BQ", "table_sessionized_partition_field")


# ----------------------
# Script Paths
# ----------------------
SCRIPT_LOCAL_PATH = "/usr/app/src/main/resources/python/gcs_to_bq_loader.py"
SCRIPT_GCS_PATH = "jobs/gcs_to_bq_loader.py"
SCRIPT_GCS_URI = f"gs://{BUCKET}/{SCRIPT_GCS_PATH}"

BASE_BATCH_NAME = "caec-load-to-bq-clickstream"
BATCH_NAME = generate_timestamped_batch_name(BASE_BATCH_NAME)


# ----------------------
# DAG Definition
# ----------------------
default_args = {
    'start_date': datetime(2025, 1, 1),
    #'retries': 2,
    #'retry_delay': timedelta(minutes=5),
    'on_failure_callback': failure_callback,
}

with DAG(
    dag_id="caec_load_to_bq_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["caec", "clickstream"],
) as dag:

    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")


    def run_gcs_to_bq_loader():
        # Define CLI args for the script
        args = [
            "python3",
            SCRIPT_LOCAL_PATH,
            "--bucket_name", BUCKET,
            "--base_prefix", BASE_PREFIX,
            "--dataset", BQ_DATASET,
            "--table", BQ_TABLE,
            "--partition_field", BQ_TABLE_PARTITION_FIELD
        ]

        env = os.environ.copy()
        env["GOOGLE_APPLICATION_CREDENTIALS"] = "/keys/caec-data-eng-sa.json"

        result = subprocess.run(args, capture_output=True, text=True, env=env)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            raise Exception("gcs_to_bq_loader.py failed")

    load_to_bq = PythonOperator(
        task_id='load_sessionized_to_bq',
        python_callable=run_gcs_to_bq_loader
    )

    load_to_bq
        

    start >> log_trigger_metadata >> load_to_bq >> end