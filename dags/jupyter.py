from airflow import DAG
from airflow.operators.python_operator import PythonOperator    
from datetime import datetime
import os

dag = DAG(
    'run_jupyter_notebook',
    schedule_interval='@once',
    start_date=datetime(2024, 4, 15),
)

def run_jupyter_task():
    os.system("cd D:\\backup\\Python\\Airflow\\.venv && Scripts\\activate.bat && python -m jupyter nbconvert --to notebook --execute D:\\backup\\Python\\Airflow\\climate change\\project.ipynb")

run_jupyter = PythonOperator(
    task_id='run_jupyter_task',
    python_callable=run_jupyter_task,
    dag=dag,
)

run_jupyter
