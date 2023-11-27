#Owner: Jagat Pradhan
#Title: Cloud Security and DevSecOps Professional

from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

URL = 'https://www.imdb.com/list/ls026690132/?sort=user_rating,desc&st_dt=&mode=detail&page=1'

data=[]

try:
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1', class_ = 'header list-name').text.strip()
    all_ws_name = soup.find('div', class_='lister-list').find_all('div', class_='lister-item mode-detail')
    
    for each_ws in all_ws_name:
        ws_name = each_ws.find('h3', class_='lister-item-header').a.text.strip()
        rank = each_ws.find('h3', class_='lister-item-header').find('span', class_='lister-item-index unbold text-primary').text
        year = each_ws.find('h3', class_='lister-item-header').find('span', class_='lister-item-year text-muted unbold').text.strip('()')
        rating = each_ws.find('div', class_='ipl-rating-widget').find('span', class_='ipl-rating-star__rating').text
        
        #append row to data
        data.append([rank,ws_name,year,rating])
    # table row names - headers   
    table_header = ['RANK', 'WEBSERIES NAME','RELEASE YEAR','iMDB RATING']
    print(tabulate(data, table_header, tablefmt='fancy_grid'))
    
except Exception as e:
    print(e)