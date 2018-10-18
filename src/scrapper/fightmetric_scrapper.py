import numpy as np
import pandas as pd
import re
import datetime
import traceback
import time
from util import name_cleaner,name_standardizer,replace_if_in_dict

import requests
from bs4 import BeautifulSoup

def url_cleaner(link):
    #TODO replace pandas
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

def event_title_scraper(soup):
    title = soup.find_all('span', class_=r'b-content__title-highlight')[0].text
    event_title = ' '.join(str(title).split())
    return event_title


def table_build(event_date,event_title,url):
    if event_date < pd.to_datetime(datetime.datetime.now()):
        df = pd.read_html(url, attrs={'class': 'b-fight-details__table'})[0]
        df.columns = [re.sub(r"\W", "", i) for i in df.columns]
        df['Fight Number'] = df.index
        df_winner = df.copy()

        #TODO build this into a function
        df_winner['Opponent'] = df_winner['Fighter'].map(lambda x: x.split('  ')[1])
        for col in ['Fighter', 'Str', 'Td', 'Sub', 'Pass']:
            df_winner[col] = df_winner[col].map(lambda x: x.split('  ')[0])

        df_loser = df.copy()
        df_loser['Opponent'] = df_loser['Fighter'].map(lambda x: x.split('  ')[0])
        for col in ['Fighter', 'Str', 'Td', 'Sub', 'Pass']:
            df_loser[col] = df_loser[col].map(lambda x: x.split('  ')[1])

        df_loser['WL'] = df_loser['WL'].map(lambda x: re.sub('win', 'loss', x))
        final_df = pd.concat([df_winner, df_loser], ignore_index=True)
        final_df['Date'] = event_date
        final_df['Event'] = event_title
        final_df['Url'] = url

        final_df = final_df.sort_values('Fight Number')

        return final_df
    else:
        pass

def table_transformer(df):
    fighter_name_standardization_dict = name_standardizer()
    df['Fighter'] = df['Fighter'].map(name_cleaner)
    df['Fighter'] = df['Fighter'].map(lambda x: replace_if_in_dict(x, fighter_name_standardization_dict))
    return df

def iterate_scrape(list):
    dfs_list = []
    for x in list:
        page = requests.get(x)
        soup = BeautifulSoup(page.content,features="lxml")
        event_date = None
        event_date = event_date_scaper(soup)
        event_title = event_title_scraper(soup)
        df = table_build(event_date,event_title,x)
        dfs_list.append(df)
    fightmetric_df = pd.concat(dfs_list,ignore_index=True)
    fightmetric_df = table_transformer(fightmetric_df)
    fightmetric_df.to_csv('../df.csv',index=False)
    return fightmetric_df



iterate_scrape(obtain_urls()[:2])
