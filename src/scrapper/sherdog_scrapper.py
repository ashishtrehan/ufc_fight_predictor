import pandas as pd
import requests
import datetime
import re
from bs4 import BeautifulSoup


def obtain_events():
    url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/recent-events/'
    url_list = []
    for x in range(1,6):
        page = requests.get(url+str(x))
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, features="lxml")
            events_table1 = soup.find_all('tr', attrs={'class': 'even'})
            events_table2 = soup.find_all('tr', attrs={'class': 'odd'})
            events_table = events_table1 + events_table2
            for i in events_table:
                event = i.find_all("a")[0].get("href").encode('ascii','ignore')
                url_list.append(event)
        else:
            pass
    return url_list

def event_date_f(soup):
    date = soup.find_all('span', attrs={'class': 'date'})[1].get_text()
    return pd.to_datetime(date)

def event_org_f(soup):
    org = soup.find_all('div', attrs={'itemprop': 'attendee'})[0]
    org = organization.find_all('span', attrs={'itemprop': 'name'})[0].get_text().encode('ascii','ignore')
    return

for x in obtain_events():
    url = 'http://www.sherdog.com'+str(x.decode("utf-8"))
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, features="lxml")
        event_date = event_date_f(soup)
        #TODO remove pandas
        if event_date < pd.to_datetime(datetime.datetime.now()):
            event_organization = soup.find_all('div', attrs={'itemprop': 'attendee'})[0]
            event_organization = event_organization.find_all('span', attrs={'itemprop': 'name'})[0].get_text().encode(
                'ascii', 'ignore')
            d = 1
            event_title = soup.find_all('div', attrs={'class': 'section_title'})[0]
            event_title = str(event_title.find_all('span', attrs={'itemprop': 'name'})[0])
            event_title = re.match(r'(<span itemprop="name">)(.*)(<br/>)(.*)(</span>)', event_title)
            event_title = event_title.group(2) + ' - ' + event_title.group(4)




