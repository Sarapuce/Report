import requests
from bs4 import BeautifulSoup
from tkinter import *

steamLoginSecure = input('steamLoginSecure cookie : ')
cookies = {'steamLoginSecure': steamLoginSecure}

start = 0
earning = 0

def convert_dollar(price):
    price = str(price).split('\t')[8]
    if price.find('€') != -1:
        return round(float(str(price)[:-1].replace(',', '.').replace('-', '0'))*1.18, 2)
    else:
        return float(str(price)[1:].replace(',', '.').replace('-', '0'))

def extract_sign(sign):
    try:
        return str(sign).split('\t')[2]
    except IndexError:
        return ''

while True:
    print('Transaction analysed : {}'.format(start))
    response = requests.get('https://steamcommunity.com/market/myhistory?start={}&count=500'.format(start), cookies=cookies).json()
    soup = BeautifulSoup(response['results_html'], 'html.parser')
    signes = soup.find_all('div', class_='market_listing_left_cell')[1:]
    prices = soup.find_all('span', class_='market_listing_price')
    
    if len(prices) == 0:
        break
        
    for i, sign in enumerate(signes):
        sign = extract_sign(sign)
        if sign == '-':
            earning += convert_dollar(prices[i])
        elif sign == '+':
            earning -= convert_dollar(prices[i])
    start += 500

print('Earning : {:.2f}$'.format(earning))
