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

month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
         'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
dateSet = set()

def dateConvert(da):
    d = da.replace(',','')
    dm = d.split(' ')
    retstr = dm[2] + '-' + month[dm[0]] + '-' + dm[1]
    return retstr


def getValues(what, body):
    scri = body.find('script', string=re.compile(what))
    iB = scri.text.find("categories:") + len("categories:")
    iE = scri.text.find(']', iB)
    categs = (scri.text)[iB : iE+1]
    dates = json.loads(categs)
    iB = scri.text.find("data:") + len("data:")
    iE = scri.text.find(']', iB)
    dann = (scri.text)[iB : iE+1]
    vals = json.loads(dann)
    coronas = {}
    for d in range(len(dates)):
        dc = dateConvert(dates[d])
        coronas[dc] = vals[d]
        dateSet.add(dc)
    return coronas


def getstate(url):
    resp = requests.get(url)
    tx = resp.text  # Access the HTML with the text property
    sup = BeautifulSoup(tx, 'lxml')  # Parse the HTML as a string
    bod = sup.find('body')
    cases =     getValues('coronavirus-cases-linear',   bod)
    active =    getValues('graph-active-cases-total',   bod)
    dead =      getValues('coronavirus-deaths-linear',  bod)
    all = []
    for d in dateSet:
        all.append({'T': d, 'A': cases[d], 'I': active[d], 'D': dead[d], 'H': None})
    all.sort(key=lambda s: s['T'], reverse=True)
    return all

statesData = []
urlUSA = "https://www.worldometers.info/coronavirus/country/us/"
response = requests.get(urlUSA)
txt = response.text  # Access the HTML with the text property
soup = BeautifulSoup(txt, 'lxml')  # Parse the HTML as a string
tab = soup.find('table', id="usa_table_countries_today")
rows = tab.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if ( not len(cols) ):
        continue
    hre = cols[1].find('a')
    if ( hre == None):
        continue
    hasRef = hre.has_attr('href')
    if (  hasRef == False ):
        continue
    subj = {}
    subj["regName"]     = hre.text.strip()
    subj["ref2"]        = hre.get('href')
    gg = cols[12].text.strip()
    subj['population']  = int(cols[12].text.strip().replace(',',''))
    subj['tests']       = int(cols[10].text.strip().replace(',',''))
    statesData.append(subj)
    ee = '{}'.format(subj)
    print(ee)

bigData = []
for su in statesData:
    regda = []
    ref = "https://www.worldometers.info" + su["ref2"]
    print(ref)
    sta = getstate(ref)
    region = {"region": su["regName"], "regData": sta, 'population': su['population'], 'tests': su['tests']}
    bigData.append(region)

json_string = json.dumps(bigData)
with open('USAmidway.json', "w") as write_file:
    write_file.write(json_string)

bigData.sort(key=lambda s: s['region'], reverse=False)
dateList = list(dateSet)
dateList.sort(reverse=True)

rectangled = []
nullCovid = {'T': None, 'A': None, 'D': None, 'H': None, 'I': None}
for r in bigData:
    mass = []
    for i in range(len(dateList)):
        nullCovid = {'T': dateList[i], 'A': None, 'D': None, 'H': None, 'I': None}
        mass.append(nullCovid)
    for d in r['regData']:
        idx = dateList.index(d['T'])
        mass[idx] = d
    rectangled.append({'region':    r['region'],
                       'popula':    r['population'],
                       'tests':     r['tests'],
                       'regData':   mass})

json_string = json.dumps(rectangled)
#with open(dataFile, "w") as write_file:
#    write_file.write(json_string)
with open('DATAS/lastUSA.json', "w") as write_file:
    write_file.write(json_string)



b = 9