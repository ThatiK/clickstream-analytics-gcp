import os
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
from airflow.operators.dummy import DummyOperator

PROJECT_ID = os.getenv("CAEC_PROJECT_ID")  
REGION = os.getenv("CAEC_REGION")  

default_args = {
    'owner': 'caec',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

with DAG(
    dag_id='caec_dbt_run',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['caec', 'dbt'],
) as dag:
    
    start = DummyOperator(task_id="start")

    run_dbt = KubernetesPodOperator(
        task_id='run_dbt',
        name='dbt-run',
        #namespace='default',
        namespace="composer-user-workloads",
        image=f'us-central1-docker.pkg.dev/{PROJECT_ID}/caec-docker/dbt-bigquery:latest',
        cmds=["/bin/bash", "-c"],
        arguments=[
            """
            dbt run --project-dir /usr/app/dbt/caec --profile caec_bigquery
            """
        ],
        env_vars={
            'CAEC_PROJECT_ID': PROJECT_ID,
            'CAEC_REGION': REGION
        },
        #service_account_name="airflow-gke-pod-sa",  
        #executor_config = {
        #    "KubernetesExecutor": {
        #        "serviceAccountName": "airflow-gke-pod-sa"
        #    }
        #},

        is_delete_operator_pod=True,
    )

    end = DummyOperator(task_id="end")

    start >> run_dbt >> end
