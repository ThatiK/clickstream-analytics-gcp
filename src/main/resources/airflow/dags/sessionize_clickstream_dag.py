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
SPARK_MAIN   = f"gs://{SCRIPTS_BKT}/spark/sessionize.py"
PROPS_URI    = f"gs://{SCRIPTS_BKT}/etc/{ENV}.properties"

default_args = {
    "owner": "caec",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="caec_sessionize_clickstream_dag",
    default_args=default_args,
    start_date=datetime(2025, 7, 1),
    schedule_interval=None,          
    catchup=False,
    tags=["caec", "clickstream"],
) as dag:

    start = DummyOperator(task_id="start")

    sessionize_batch = DataprocCreateBatchOperator(
        task_id="sessionize_batch",
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
        batch_id="caec-sessionize-{{ ts_nodash }}",        # unique per run (includes H M S)
        region=REGION,
        project_id=PROJECT_ID,
    )

    end = DummyOperator(task_id="end")

    start >> sessionize_batch >> end
