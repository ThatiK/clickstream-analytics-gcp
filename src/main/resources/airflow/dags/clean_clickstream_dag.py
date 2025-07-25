import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
#from airflow.providers.google.cloud.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator

# Airflow Variables
PROJECT_ID   = os.getenv("CAEC_PROJECT_ID")
REGION       = os.getenv("CAEC_REGION")
SCRIPTS_BKT  = os.getenv("CAEC_SCRIPTS_BUCKET")     # "caec-prod-scripts"
ENV          = os.getenv("CAEC_ENV")                # "prod" | "dev"

# GCS URIs
SPARK_MAIN   = f"gs://{SCRIPTS_BKT}/spark/clean_clickstream.py"
PROPS_URI    = f"gs://{SCRIPTS_BKT}/etc/{ENV}.properties"

def generate_timestamped_batch_name(base_name):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}-{ts}"

BASE_BATCH_NAME = "caec-clean-clickstream"
BATCH_NAME = generate_timestamped_batch_name(BASE_BATCH_NAME)

# Default DAG args
default_args = {
    "owner": "caec",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    #"retries": 1,
    #"retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="caec_clean_clickstream_dag",
    default_args=default_args,
    start_date=datetime(2025, 7, 1),
    schedule_interval=None,
    catchup=False,
    tags=["caec", "clickstream"],
) as dag:

    start = DummyOperator(task_id="start")

    # Dataproc Serverless batch task 
    clean_batch = DataprocCreateBatchOperator(
        task_id="clean_clickstream_batch",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": SPARK_MAIN,
                "python_file_uris": [PROPS_URI],          
                "args": [
                    "--conf", f"{ENV}",                   
                ],
            },
            "environment_config": {
                "execution_config": {
                    "service_account": f"caec-data-eng-sa@{PROJECT_ID}.iam.gserviceaccount.com"
                }
            },
        },
        batch_id=BATCH_NAME,
        region=REGION,
        project_id=PROJECT_ID,
    )

    #trigger_sessionize = TriggerDagRunOperator(
    #    task_id="trigger_sessionize_dag",
    #    trigger_dag_id="caec_sessionize_clickstream_dag",
    #    wait_for_completion=True,
    #    reset_dag_run=True,
    #    execution_date="{{ ds }}",
    #)

    end = DummyOperator(task_id="end")

    # DAG flow
    start >> clean_batch >> end
