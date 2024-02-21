from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import requests
from bs4 import BeautifulSoup

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 20),
    'retries': 1,
}

dag = DAG(
    'flipkart_scrape_to_csv',
    default_args=default_args,
    description='Scrape Flipkart mobile data and save to CSV',
    schedule_interval='@daily',
)

def scrape_and_save_to_csv():
    base_url = 'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DAPPLE&page='

    def mobile_name(doc):
        names = [tag.text.strip() for tag in doc.find_all('div', class_='_4rR01T')]
        return names

    def prices(doc):
        price_links = [tag.text.strip() for tag in doc.find_all('div',class_='_30jeq3 _1_WHN1')]
        return price_links

    def percentage_off(doc):
        off_links = [{'Percentage off': tag.text.strip()} for tag in doc.find_all('div',class_='_3Ay6Sb')]
        return off_links  

    def rating(doc):
        all_ratings = [tag.text.strip() for tag in doc.find_all('div', class_='_3LWZlK')]
        return all_ratings

    def mobile_description(doc):
        mobile_info_links = [tag.text.strip() for tag in doc.find_all('ul', class_='_1xgFaf')]
        return mobile_info_links

    def for_all_pages(page_no):
        page_no_url = base_url +  str(page_no)
        response = requests.get(page_no_url)
        
        if response.status_code != 200:
            print('Status code:', response.status_code)
            return None
        
        doc =  BeautifulSoup(response.text, 'html.parser')
        mobile_names = mobile_name(doc)
        all_prices = prices(doc)
        all_ratings = rating(doc)
        mobile_descriptions = mobile_description(doc)
        data = {
            'Name': mobile_names,
            'Prices': all_prices,
            'Ratings': all_ratings,
            'Description': mobile_descriptions
        }
        
        return pd.DataFrame(data)

    def all_info(num_of_pages):
        all_dfs = []
        for i in range(1, num_of_pages+1):
            df = for_all_pages(page_no=i)
            if df is not None:
                all_dfs.append(df)
        
        if not all_dfs:
            print("No data fetched.")
            return None
        
        merge = pd.concat(all_dfs)
        return merge

    # Calling the function to fetch data and save as CSV
    all_info_df = all_info(20)
    if all_info_df is not None:
        all_info_df.to_csv('D:\\Python\\Airflow\\all_info_final.csv', index=None)
        
        print("Data fetched and saved as all_info_final.csv")

scrape_task = PythonOperator(
    task_id='scrape_and_save_to_csv',
    python_callable=scrape_and_save_to_csv,
    dag=dag,
)

scrape_task
