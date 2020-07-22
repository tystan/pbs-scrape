



# make sure you have set HTTPS_PROXY system variable if relevant
# $ pip3 install requests
# $ pip3 install beautifulsoup4

import requests
import pprint
from bs4 import BeautifulSoup
import pandas
import os
import numpy as np
import re

print(os.getcwd())
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
print(os.getcwd())

pbs_ics = pandas.read_csv('pbs-item-list.csv', encoding='latin-1')
print(pbs_ics)

item_codes = pbs_ics['ITEM_CODE']
this_ic = item_codes[1].lstrip("0")

def strip_0(x):
    return x.lstrip('0')

# test: strip_0(item_codes[1])

pbs_ics.apply(lambda x: strip_0(x['ITEM_CODE']), axis=1)


pbs_ics['stripped_ic'] = pbs_ics.apply(lambda x: strip_0(x['ITEM_CODE']), axis=1)
pbs_ics['web_descrip'] = ''

nrow = len(pbs_ics)

for i in range(0, nrow):
    this_ic = pbs_ics['stripped_ic'][i]
    URL = 'http://www.pbs.gov.au/medicine/item/' + this_ic
    page = requests.get(URL)
    if not(200 <= page.status_code <= 299):
        print("ERROR downloading PBS_ITEM page", i, "of", nrow, "(", URL, ")")
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='content')
        dets = results.find_all('span', class_='form-strength')
        descrip_str = ''
        for det in dets:
            descrip_str = descrip_str + det.text
            # print(det, end='\n'*2)
            # print(det.find('form-strength'))
        if descrip_str == '':
            print("Downloaded PBS_ITEM page ", i, " of ", nrow, "| WARNING no drug description found for" + this_ic)
        else:
            pbs_ics['web_descrip'][i] = descrip_str
            print("Downloaded PBS_ITEM page ", i, " of ", nrow, "|", descrip_str)


# dims of data frame
pbs_ics.shape
# data types of data frame
pbs_ics.dtypes
# summary
pbs_ics.describe()

# testing:
# rem_whitespace(pbs_ics['web_descrip'][353])

def rem_whitespace(x):
    return re.sub(r"\s+", " ", x)

def end_with_qnty(x):
    primary_search_str = r",\s[\d\.\sxmLg]+"
    pack_search_str = r"(sachet|roll|syringe|ampoule|vial|box|actuation|pack|can|pen device|cartridge|injection|bottle|carton|unit dose|dual chamber syringe|sheet)?s?$"
    search_str = primary_search_str + pack_search_str # or: "".join([primary_search_str, pack_search_str])
    search_obj = re.search(search_str, x)
    if search_obj is None:
        return ""
    else:
        return search_obj[0] # [0] extracts match text from match object

def is_not_empty_str(x):
    return (x != "")

def add_qnty(x, y):
    if is_not_empty_str(end_with_qnty(x)):
        return x
    else:
        y0 = end_with_qnty(y)
        if is_not_empty_str(y0):
            return "".join([x, y0]) 
        else:
            return x



# remove the tabs and newlines
pbs_ics['web_descrip'] = list(map(rem_whitespace, pbs_ics['web_descrip']))

# search descriptions for quantities
pbs_ics['web_qnty'] = list(map(end_with_qnty, pbs_ics['web_descrip']))
pbs_ics['fs_qnty'] = list(map(end_with_qnty, pbs_ics['FORM/STRENGTH']))
pbs_ics['form_strength_new'] = list(map(add_qnty, pbs_ics['FORM/STRENGTH'], pbs_ics['web_descrip']))
pbs_ics


# pbs_ics.drop('web_descrip2', axis = 1, inplace=True)

# check: pbs_ics['web_descrip'][353]

pbs_ics.to_csv('pbs-list-plus-web-decrip.csv')

