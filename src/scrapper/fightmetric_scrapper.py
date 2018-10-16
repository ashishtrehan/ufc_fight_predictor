import numpy as np
import pandas as pd
import re
import datetime
import traceback
import time

import requests
from bs4 import BeautifulSoup




page = requests.get('http://www.fightmetric.com/statistics/events/completed?page=all')
soup = BeautifulSoup(page.content,features="lxml")

# urls_list = []
# all_links = soup.find_all("a")
# for link in all_links:
#     link_text = link.get("href")
#     if not pd.isnull(link_text):
#         try:
#             link_text = link_text.encode('ascii','ignore') #fix issue of str(link_text) not working due to unknown unicode character
#         except:
#             print (link_text)
#         if str.find(str(link_text),r'http://www.fightmetric.com/event-details/') != -1:
#             urls_list.append(link_text)

print (soup)