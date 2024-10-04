from datetime import datetime
import os

import minio
from airflow import DAG
from airflow.operators.python import PythonOperator


dag = DAG(
    dag_id='ingest-sinan-pipeline',
    description='',
    default_args={
        'owner': 'admin',
        'retries': 1,
        'start_date': datetime(2024, 10, 3),
        'catchup': False,
    },
    tags=['ingest-sinan']
)


client = minio.Minio(
        os.environ.get('MINIO_ENDPOINT'),
        access_key=os.environ.get('MINIO_ACCESS_KEY'),
        secret_key=os.environ.get('MINIO_SECRET_KEY'),
        secure=False  # Adjust based on your MinIO configuration
    )


def _download_sinan_data():
    pass


start = PythonOperator(
    task_id="start",
    python_callable=lambda: print("Jobs started"),
    dag=dag
)


download_files_task = PythonOperator(
    task_id='Download_dbc_files',
    python_callable=_download_sinan_data,
    dag=dag
)


end = PythonOperator(
    task_id="end",
    python_callable=lambda: print("Jobs completed successfully"),
    dag=dag
)


start >> download_files_task >> end
