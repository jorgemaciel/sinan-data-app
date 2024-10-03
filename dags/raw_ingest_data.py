from datetime import datetime
import os
import urllib.request

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


def get_dbc_file(ano, client):
    url = f'ftp://ftp.datasus.gov.br/dissemin/publicos/SINAN/DADOS/PRELIM/ANIMBR{ano}.dbc'
    filename = f'ANIMBR{ano}.dbc'

    urllib.request.urlretrieve(url, filename)

    data_dir = os.environ.get('MINIO_DATA_SUS_FOLDER')

    client.fput_object(
        os.environ.get('MINIO_BUCKET_NAME'),
        f"{data_dir}/{filename}",
        filename,
        content_type='application/octet-stream'
    )

    # Delete the local file
    os.remove(filename)


def _download_dbc_file():
    dates = ['2020', '2021', '2022', '2023']
    client = minio.Minio(
        os.environ.get('MINIO_ENDPOINT'),
        access_key=os.environ.get('MINIO_ACCESS_KEY'),
        secret_key=os.environ.get('MINIO_SECRET_KEY'),
        secure=False  # Adjust based on your MinIO configuration
    )

    # Check if bucket exists, create if not
    if not client.bucket_exists(os.environ['MINIO_BUCKET_NAME']):
        client.make_bucket(os.environ['MINIO_BUCKET_NAME'])

    for date in dates:
        date = date[-2:]  # Extract the last two digits of the year
        get_dbc_file(date, client)


start = PythonOperator(
    task_id="start",
    python_callable=lambda: print("Jobs started"),
    dag=dag
)


download_files_task = PythonOperator(
    task_id='Download_dbc_files',
    python_callable=_download_dbc_file,
    dag=dag
)


end = PythonOperator(
    task_id="end",
    python_callable=lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> download_files_task >> end
