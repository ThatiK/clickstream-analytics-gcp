import os
from datetime import datetime, timedelta
import uuid
import configparser

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator


def failure_callback(context):
    dag_run = context.get("dag_run")
    task_instance = context.get("task_instance")
    print(f"[ALERT] Task {task_instance.task_id} in DAG {dag_run.dag_id} failed.")

def generate_timestamped_batch_name(base_name):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}-{ts}"


# ----------------------
# Load Config
# ----------------------
ENV = os.getenv("CAEC_ENV", "dev")  # default to dev
CONFIG_PATH = f"/usr/app/src/main/resources/etc/{ENV}.properties"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

PROJECT_ID = config.get("COMMON", "project_id")
REGION = config.get("COMMON", "region")
BUCKET = config.get("COMMON", "bucket")
SERVICE_ACCOUNT = config.get("COMMON", "sa_airflow_email")

RAW_EVENTS_PATH = config.get("PATHS", "raw_events")
CLEAN_EVENTS_PATH = config.get("PATHS", "clean_events")

# ----------------------
# Script Paths
# ----------------------
SCRIPT_LOCAL_PATH = "/usr/app/src/main/resources/spark/clean_clickstream.py"
SCRIPT_GCS_PATH = "jobs/clean_clickstream.py"
SCRIPT_GCS_URI = f"gs://{BUCKET}/{SCRIPT_GCS_PATH}"

BASE_BATCH_NAME = "caec-clean-clickstream"
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






# ----------- Define DAG -----------
with DAG(
    dag_id="caec_clean_clickstream_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["caec", "clickstream"],
) as dag:
    
    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")

    with TaskGroup("upload_and_submit_job", tooltip="Upload and Submit Spark Job") as group:

        # Upload the Spark script to GCS
        upload_script = LocalFilesystemToGCSOperator(
            task_id="upload_clean_clickstream_script",
            src=SCRIPT_LOCAL_PATH,
            dst=SCRIPT_GCS_PATH,
            bucket=BUCKET,
            mime_type="text/x-python"
        )

        # Submit Dataproc Serverless batch job
        submit_batch = DataprocCreateBatchOperator(
            task_id="submit_clean_clickstream_batch",
            batch={
                "pyspark_batch": {
                    "main_python_file_uri": SCRIPT_GCS_URI,
                    "args": [
                        "--input", RAW_EVENTS_PATH,
                        "--output", CLEAN_EVENTS_PATH
                    ]
                },
                "environment_config": {
                    "execution_config": {
                        "service_account": SERVICE_ACCOUNT
                    }
                }
            },
            batch_id=BATCH_NAME,
            region=REGION,
            project_id=PROJECT_ID,
            gcp_conn_id="google_cloud_default"
        )

        upload_script >> submit_batch

    trigger_sessionize = TriggerDagRunOperator(
        task_id="trigger_sessionize_dag",
        trigger_dag_id="caec_sessionize_clickstream_dag",
        wait_for_completion=True,  
        reset_dag_run=True,         
        execution_date="{{ ds }}",  
    )

    start >> group >> trigger_sessionize >> end

