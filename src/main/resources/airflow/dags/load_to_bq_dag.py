import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.dummy import DummyOperator

# Airflow Variables
PROJECT_ID      = os.getenv("CAEC_PROJECT_ID")
REGION          = os.getenv("CAEC_REGION")
SCRIPTS_BUCKET  = os.getenv("CAEC_SCRIPTS_BUCKET")         
BQ_DATASET      = os.getenv("CAEC_BQ_DATASET", "caec_analytics")
ENV             = os.getenv("CAEC_ENV")                    


GCS_SOURCE_URI  = f"gs://{SCRIPTS_BUCKET}/sessionized/events/event_date_part={{ ds_nodash }}/*.parquet"
BQ_TABLE        = f"{PROJECT_ID}.{BQ_DATASET}.clickstream_sessions"

def generate_timestamped_batch_name(base_name):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}-{ts}"

BASE_BATCH_NAME = "caec-load-to-bq-clickstream"
BATCH_NAME = generate_timestamped_batch_name(BASE_BATCH_NAME)

default_args = {
    "owner": "caec",
    "email_on_failure": False,
    "email_on_retry": False,
    #"retries": 1,
    #"retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="caec_load_clickstream_to_bq_dag",
    start_date=datetime(2025, 7, 1),
    schedule_interval=None,            # typically triggered by upstream DAG
    catchup=False,
    default_args=default_args,
    tags=["caec", "clickstream", "bq"],
) as dag:

    start = DummyOperator(task_id="start")

    # Load from GCS into BigQuery
    load_to_bq = GCSToBigQueryOperator(
        task_id="gcs_to_bq",
        bucket=SCRIPTS_BUCKET,
        source_objects=[f"sessionized/events/event_date_part={{ ds_nodash }}/*.parquet"],
        destination_project_dataset_table=BQ_TABLE,
        source_format="PARQUET",
        write_disposition="WRITE_TRUNCATE",          
        time_partitioning={"type": "DAY"},
        gcp_conn_id="google_cloud_default",          
    )

    end = DummyOperator(task_id="end")

    start >> load_to_bq >> end
