import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import re




def flipkart_func():
    url = 'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DAPPLE&page='
    
    chrome_path = "D:\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Use the Service class to set the executable path
    service = Service(chrome_path)

    # Pass the service object to the webdriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    info = (driver.find_element(By.XPATH,'//*[@id="container"]/div/div[3]/div/div[2]/div[26]/div/div/span[1]').text)
    print(info)
    # Example string
    page_info = info

    # Use regular expression to extract the numeric value
    match = re.search(r'\b(\d+)\b.*\b(\d+)\b', page_info)
    numeric_value = match.group(2)
    # Convert the numeric value to an integer if needed
    numeric_value = int(numeric_value)
    link = []
    names = []
    prices = []
    percentage_off = []
    ratings = []
    description = []
    reviews = []


    for pg in range(numeric_value+1):
        driver.get(url + str(pg))
        time.sleep(3)
        container = driver.find_elements(By.CLASS_NAME,'_1fQZEK')
        #links
        for li in container:
            try:
                link.append(li.get_attribute('href'))
            except NoSuchElementException:
                link.append('No Link Available')
        #mobile names
        for name in container:
            try:
                names.append(name.find_element(By.CLASS_NAME,'_4rR01T').text.strip())
            except NoSuchElementException:
                names.append('No Mobile Name Available')
        #Prices
        for pri in container:
            try:
                prices.append(pri.find_element(By.CLASS_NAME,'_30jeq3').text.strip())
            except NoSuchElementException:
                prices.append('No Price Available')
        #Percentage off
        for off in container:
            try:
                percentage_off.append(off.find_element(By.CLASS_NAME, '_3Ay6Sb').text)
            except NoSuchElementException:
                percentage_off.append('No Percentage Off')
        #Ratings
        for rat in container:
            try:
                ratings.append(rat.find_element(By.CLASS_NAME,'_3LWZlK').text)
            except NoSuchElementException:
                ratings.append('No Ratings Available')
        #desc
        for desc in container:
            try:
                description.append(desc.find_element(By.CLASS_NAME,'_1xgFaf').text)
            except NoSuchElementException:
                description.append('No Description Available')
        #reviews
        for rev in container:
            try:
                reviews.append(rev.find_element(By.CLASS_NAME,'_2_R_DZ').text)
            except NoSuchElementException:
                reviews.append('No reviews Available')

        #getting all the information in a dictionary
    data_new = {'Name': names,  
       'Prices':prices,
       'ratings':ratings,
       '% OFF':percentage_off,
       'Ratings and Reviews':reviews,
       'Description':description,
       'Product Link':link}
    df = pd.DataFrame(data_new)
    csv_data = df.to_csv('D:\Python\Airflow\dags\flipkart_data.csv', index=False)    
    return csv_data

if __name__ == '__main__':
    flipkart_func()
