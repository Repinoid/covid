# -*- coding: cp1251 -*
import datetime
from bs4 import BeautifulSoup
import lxml
import requests
import wget
import urllib.request
import json
import os
import csv
import re

url = "rus1124.tab"
#encoding = 'utf-8'
with open(url, "r", encoding = 'utf-8') as fi:
    str = fi.read()


s = BeautifulSoup(str, 'lxml')  # Parse the HTML as a string
regT = s.find('table')
rows = regT.find_all('tr')


#with open("'co.j", "w",  encoding='utf-8') as write_file:
 #   write_file.write(rd)
#exit()


data = []
for row in rows:
    cols = row.find_all('td')
    if ( not len(cols) ):
        continue
    subj = {}
    subj["regName"]     =       cols[0].text.strip()
 #   subj["ref2"]        =       cols[0].find('a').get('href')
#    subj["privito"]     =       int(cols[5].text.strip().replace(' ', ''))
    subj["privProc"]    =       float(cols[3].text.strip().replace('%', ''))

    data.append(subj)
    ee = '{}'.format(subj)
    print(ee)
with open("rus1124Ukol.json", "w") as write_file:
    json.dump(data, write_file)