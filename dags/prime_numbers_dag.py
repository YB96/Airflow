from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def print_prime_numbers():
    prime_numbers = [num for num in range(1, 101) if is_prime(num)]
    print("Prime Numbers from 1 to 100:", prime_numbers)
    return prime_numbers

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 10,
}

dag_id = 'prime_numbers_dag'

with DAG(
    dag_id,
    default_args=default_args,
    schedule_interval=None,  # You can set the schedule_interval based on your requirements
) as dag:

    print_prime_numbers_task = PythonOperator(
        task_id='print_prime_numbers_task',
        python_callable=print_prime_numbers,
    )

    print_prime_numbers_task
