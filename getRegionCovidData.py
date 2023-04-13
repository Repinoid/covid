# -*- coding: cp1251 -*
from bs4 import BeautifulSoup
import lxml
import requests
import wget
import urllib.request
import json
import os
from urusas import population

def getRegionCovidData(regURL):
    region_data = []
    ref = "https://russian-trade.com/coronavirus-russia/" + regURL
    response = requests.get(ref)
    txt = response.text  # Access the HTML with the text property
    soup = BeautifulSoup(txt, 'lxml')  # Parse the HTML as a string
    region_table = soup.find('table', id='curs_special')
    rows = region_table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if (not len(cols)):
            continue
        subj = {}
        t = cols[0].text.strip()                    # date originally D-M-Y
        s = t.split('.')
        a = "{}-{}-{}".format(s[2], s[1], s[0])     # convert to date Y-M-D
        subj["T"] = a
        subj["A"] = int(cols[1].text.strip())       # all, new covidints
        subj["D"] = int(cols[2].text.strip())       # dead
        subj["H"] = int(cols[3].text.strip())       # healed
        subj["I"] = int(cols[4].text.strip())       # still ill
        region_data.append(subj)
    return region_data

rgd = getRegionCovidData("moskva")

a = 9