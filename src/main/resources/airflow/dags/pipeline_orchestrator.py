from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from datetime import datetime


default_args = {
    'owner': 'caec',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

with DAG(
    dag_id="caec_pipeline_orchestrator",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    description="Master DAG to orchestrate clean → sessionize → load → dbt steps",
) as dag:
    
    start = DummyOperator(task_id="start")

    trigger_clean = TriggerDagRunOperator(
        task_id="trigger_clean",
        trigger_dag_id="caec_clean_clickstream_dag",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    trigger_sessionize = TriggerDagRunOperator(
        task_id="trigger_sessionize",
        trigger_dag_id="caec_sessionize_clickstream_dag",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    trigger_load_to_bq = TriggerDagRunOperator(
        task_id="trigger_load_to_bq",
        trigger_dag_id="caec_load_to_bq_clickstream_dag",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    trigger_dbt = TriggerDagRunOperator(
        task_id="trigger_dbt_run",
        trigger_dag_id="caec_dbt_run",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    end = DummyOperator(task_id="end")

    start >> trigger_clean >> trigger_sessionize >> trigger_load_to_bq >> trigger_dbt >> end
