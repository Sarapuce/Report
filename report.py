import requests
from bs4 import BeautifulSoup
import _thread
from tkinter import *
from tkinter import ttk

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

class History():
    def __init__(self):
        self.earning = 0
        self.cookies = {'steamLoginSecure': ''}
        
    def update_cookie(self, cookie):
        self.cookies['steamLoginSecure'] = cookie
        
    def reset_earning(self):
        self.earning = 0
        
    def get_history(self, earningString):
            start = 0
            self.reset_earning()
            while True:
                print(start)
                response = requests.get('https://steamcommunity.com/market/myhistory?start={}&count=500'.format(start), cookies=self.cookies).json()
                soup = BeautifulSoup(response['results_html'], 'html.parser')
                signes = soup.find_all('div', class_='market_listing_left_cell')[1:]
                prices = soup.find_all('span', class_='market_listing_price')

                if len(prices) == 0:
                    if start == 0:
                        earningString.set('Wrong steam cookie or empty history')
                    break

                for i, sign in enumerate(signes):
                    sign = extract_sign(sign)
                    if sign == '-':
                        self.earning += convert_dollar(prices[i])
                    elif sign == '+':
                        self.earning -= convert_dollar(prices[i])
                    earningString.set('{:.2f}$'.format(self.earning))
                start += 500

def cookie_updated(*args):
    history.update_cookie(steamLoginSecure.get())

def start_history():
    _thread.start_new_thread(lambda : history.get_history(earningString), ())

window = Tk()
window.title('Steam Market history retriever')
history = History()

steamLoginSecure = StringVar() 
steamLoginSecure.set('steamLoginSecure')
steamLoginSecure.trace('w', cookie_updated)

earningString = StringVar()
earningString.set('0.00$')
earningLabel = Label(window, textvariable = earningString)

input_steamLoginSecure = Entry(window, textvariable = steamLoginSecure, width=70)

btn_start = Button(window, text='Get my history', command=start_history)

input_steamLoginSecure.pack()
btn_start.pack()
earningLabel.pack()

window.mainloop()
