import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from airflow.operators.dummy import DummyOperator

# Airflow Variables 
PROJECT_ID   = os.getenv("CAEC_PROJECT_ID")
REGION       = os.getenv("CAEC_REGION")
SCRIPTS_BKT  = os.getenv("CAEC_SCRIPTS_BUCKET")   
ENV          = os.getenv("CAEC_ENV")              

# GCS URIs 
SPARK_MAIN   = f"gs://{SCRIPTS_BKT}/spark/load_to_bq_clickstream.py"
PROPS_URI    = f"gs://{SCRIPTS_BKT}/etc/{ENV}.properties"
CONNECTOR = "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.29.0.jar"


def generate_timestamped_batch_name(base_name):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}-{ts}"

BASE_BATCH_NAME = "caec-lot-to-bq-clickstream"
BATCH_NAME = generate_timestamped_batch_name(BASE_BATCH_NAME)


default_args = {
    "owner": "caec",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    #"retries": 1,
    #"retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="caec_load_to_bq_clickstream_dag",
    default_args=default_args,
    start_date=datetime(2025, 7, 1),
    schedule_interval=None,          
    catchup=False,
    tags=["caec", "clickstream"],
) as dag:

    start = DummyOperator(task_id="start")

    sessionize_batch = DataprocCreateBatchOperator(
        task_id="load_to_bq_batch",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": SPARK_MAIN,
                "python_file_uris": [PROPS_URI],           
                "args": [
                    "--conf", f"{ENV}",                    
                ],
                "jar_file_uris": [CONNECTOR],
            },
            "runtime_config": {
                "version": "2.1"  
            },
            "environment_config": {
                "execution_config": {
                    "service_account": f"caec-data-eng-sa@{PROJECT_ID}.iam.gserviceaccount.com"
                }
            },
        },
        batch_id=BATCH_NAME,        # unique per run (includes H M S)
        region=REGION,
        project_id=PROJECT_ID,
    )

    end = DummyOperator(task_id="end")

    start >> sessionize_batch >> end
