from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

# Define default_args dictionary to pass to the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 11, 30),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate a DAG
dag = DAG(
    'my_simple_dag',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval=timedelta(days=1),  # Set the interval at which to run the DAG (daily in this case)
)

# Define tasks
task1 = DummyOperator(task_id='task1', dag=dag)
task2 = DummyOperator(task_id='task2', dag=dag)
task3 = DummyOperator(task_id='task3', dag=dag)

# Define task dependencies
task1 >> task2
task1 >> task3
