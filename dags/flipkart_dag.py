# flipkart_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta
from dags.flipkart_selenium import flipkart_func


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 10,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'flipkart_dag',
    default_args=default_args,
    description='A simple DAG to run a Python script and save data to CSV',
    max_active_runs=32,  # Set your desired value here
    concurrency=16,
    schedule_interval=timedelta(days=1),
)

run_python_task = PythonOperator(
    task_id='run_python_script',
    python_callable=flipkart_func,
    dag=dag,
    docker_command="D:\Python\Airflow\dags\flipkart.py"
)

# Add a PostgresOperator to execute SQL queries
view_csv_in_sql = PostgresOperator(
    task_id='view_csv_in_sql',
    postgres_conn_id='postgres_default',  # Use the connection ID defined in Airflow
    sql="COPY your_table FROM 'D:\Python\Airflow\dags\flipkart_data.csv' DELIMITER ',' CSV HEADER;",
    dag=dag,
)

run_python_task >> view_csv_in_sql
