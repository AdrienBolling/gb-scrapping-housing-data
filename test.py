import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

df = pd.read_csv('gb-postal-codes.csv')

edge_option = webdriver.EdgeOptions()
edge_option.use_chromium = True
# edge_option.add_argument("headless")

s = Service('./msedgedriver.exe')
browser = webdriver.Edge(service=s, options=edge_option)
browser.create_options()

url_root = 'https://www.home.co.uk/guides/house_prices.htm?location='

type_list = ['Flat','Terraced','Semi-detached','Detached']
df_types = []
for types in type_list:
    df_types.append(pd.DataFrame(columns=['postal_code', 'number', 'average_price', 'median_price']))

def parse_and_get(postal_code):
    url = url_root+str(postal_code)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    tables = soup.find_all(class_='table table--plain indented-left')
    res = (str(tables[3]).split('<tr>')[2:])
    for i in range(len(type_list)):
        line = res[i].split('</td>')
        number = int(line[1].strip('\n<td>'))
        average = line[2].strip('\n<td>£').strip(',')
        median = line[3].strip('\n<td>£').strip(',')
        df_types[i].loc[df_types[i].shape[0]] = [postal_code, number, average, median]


df['postal_code'].apply(parse_and_get)


for i in range(len(df_types)):
    df_types[i].to_csv('gb-'+type_list[i].lower+'.csv')
browser.quit()