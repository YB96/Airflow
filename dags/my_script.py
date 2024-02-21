# my_script.py
import pandas as pd

def run_task():
    # Your Python script logic here
    data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)
    
    # Save data to CSV file
    df.to_csv('/usr/local/airflow/dags/output.csv', index=False)
    
if __name__ == '__main__':
    run_task()
