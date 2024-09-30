import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import (
    SparkSubmitOperator,
)

dag = DAG(
    dag_id="sparking_flow",
    default_args={
        "owner": "Yusuf Ganiyu",
        "start_date": airflow.utils.dates.days_ago(1)
    },
    schedule_interval="@daily"
)

start = PythonOperator(
    task_id="start",
    python_callable=lambda: print("Jobs started"),
    dag=dag
)

python_job = SparkSubmitOperator(
    task_id="python_job",
    conn_id="spark-conn",
    application="jobs/wordcountjob.py",
    dag=dag
)

python_test_job = SparkSubmitOperator(
    task_id="test_job",
    conn_id="spark-conn",
    application="jobs/teste.py",
    dag=dag
)

end = PythonOperator(
    task_id="end",
    python_callable=lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> [python_job, python_test_job] >> end
