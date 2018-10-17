import numpy as np
import pandas as pd
import re
import datetime
import traceback
import time

import requests
from bs4 import BeautifulSoup

def url_cleaner(link):
    if not pd.isnull(link):
        try:  # fix issue of str(link_text) not working due to unknown unicode character
            if str.find(link,r'http://www.fightmetric.com/event-details/') != -1:
                return link
            else:
                pass
        except:
            pass


def obtain_urls():
    #Obtain all fightmetric urls to loop through
    page = requests.get('http://www.fightmetric.com/statistics/events/completed?page=all')
    soup = BeautifulSoup(page.content,features="lxml")
    urls_list = []
    all_links = soup.find_all("a")
    text = [url_cleaner(x.get("href")) for x in all_links
            if url_cleaner(x.get("href")) is not None]
    return text

def event_date_scaper(soup):
    for i in soup.find_all('ul'):
        for idx, li in enumerate(i.findChildren('li')):
            if idx in range(3):
                if str.find(str(li.text), r'Date:') != -1:
                    event_date = ' '.join(str(li.text).split())  # split then rejoin to strip whitespace properly
                    event_date = event_date[6:]
                    #TODO replace pandas with datetime or dateutil package
                    event_date = pd.to_datetime(event_date)
    return event_date

def iterate_scrape(list):
    for x in list:
        page = requests.get(x)
        soup = BeautifulSoup(page.content)
        event_date = None
        event_date = event_date_scaper(soup)
        event_title = soup.find_all('span', class_=r'b-content__title-highlight')[0].text
        event_title = ' '.join(str(event_title).split())
        print (event_title)




iterate_scrape(obtain_urls())
