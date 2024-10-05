from datetime import datetime
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from minio import Minio
from minio.error import S3Error
from pysus.ftp.databases.sinan import SINAN


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


client = Minio(
        os.environ.get('MINIO_ENDPOINT'),
        access_key=os.environ.get('MINIO_ACCESS_KEY'),
        secret_key=os.environ.get('MINIO_SECRET_KEY'),
        secure=False  # Adjust based on your MinIO configuration
    )


def _download_sinan_data():
    sinan = SINAN().load()
    files = sinan.get_files(dis_code='ANIM')
    sinan.download(files)


def find_anim_directories(base_path='/home/airflow/pysus'):
    anim_directories = []
    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path) and entry.startswith('ANIMBR'):
            anim_directories.append(full_path)
    return anim_directories


def _copy_parquet_to_raw(src_directories=find_anim_directories(), minio_bucket=os.environ.get('MINIO_BUCKET_NAME'), minio_client=client):

    for src_directory in src_directories:
        for root, _, files in os.walk(src_directory):
            for file in files:
                if file.endswith('.parquet'):
                    local_file_path = os.path.join(root, file)
                    # Create a relative path for MinIO
                    minio_file_path = os.path.relpath(
                        local_file_path, src_directory
                    )

                    try:
                        # Upload the file to MinIO
                        minio_client.fput_object(
                            minio_bucket, minio_file_path, local_file_path
                        )
                        print(f"Uploaded: {minio_file_path}")
                    except S3Error as e:
                        print(f"Error occurred: {e}")


start = PythonOperator(
    task_id="start",
    python_callable=lambda: print("Jobs started"),
    dag=dag
)


download_files_task = PythonOperator(
    task_id='Download_sinan_files',
    python_callable=_download_sinan_data,
    dag=dag
)


copy_parquet_to_raw_task = PythonOperator(
    task_id='Copy_parquet_to_raw',
    python_callable=_copy_parquet_to_raw,
    dag=dag
)


end = PythonOperator(
    task_id="end",
    python_callable=lambda: print("Jobs completed successfully"),
    dag=dag
)


start >> download_files_task >> copy_parquet_to_raw_task >> end
