# -*- coding: cp1251 -*
from bs4 import BeautifulSoup
import lxml
import requests
import wget
import urllib.request
import json
import os
from urusas import population


url = "https://russian-trade.com/coronavirus-russia/moskva/"
response = requests.get(url)
txt = response.text  # Access the HTML with the text property
soup = BeautifulSoup(txt, 'lxml')  # Parse the HTML as a string
regT = soup.find('table', id='curs_special')
rows = regT.find_all('tr')
rowLastDat = rows[1]
cols = rowLastDat.find_all('td')
lastDat = cols[0].text.strip()
dataFile = 'DATAS/' + lastDat + ".json"
#if os.path.isfile(dataFile):
 #   exit()                  # stop if last date already exists

url = 'https://russian-trade.com/coronavirus-russia/'
response = requests.get(url)
txt = response.text  # Access the HTML with the text property
soup = BeautifulSoup(txt, 'lxml')  # Parse the HTML as a string
data = []

regT = soup.find('table', id = 'curs_special')
rows =  regT.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    if ( not len(cols) ):
        continue
    subj = {}
    subj["regName"]     =       cols[1].text.strip()
    subj["ref2"]        =       cols[1].find('a').get('href')
    subj["allZ"]        =       cols[2].text.strip().partition('(')[0]
    subj["trup"]        =       cols[3].text.strip().partition('(')[0]
    subj["heal"]        =       cols[4].text.strip().partition('(')[0]
    subj["zaraza"]      =       cols[5].text.strip().partition('(')[0]
    data.append(subj)
    ee = '{}'.format(subj)
    print(ee)
#with open("'covidRUS.json", "w") as write_file:
 #   json.dump(data, write_file)
bigData = []
dateSet = set()
for su in data:
    regda = []
    ref = "https://russian-trade.com" + su["ref2"]
    response = requests.get(ref)
    txt = response.text  # Access the HTML with the text property
    soup = BeautifulSoup(txt, 'lxml')  # Parse the HTML as a string
    regT = soup.find('table', id='curs_special')
    rows = regT.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if (not len(cols)):
            continue
        subj = {}
        t = cols[0].text.strip()        # date originally D-M-Y
        s = t.split('.')
        a = "{}-{}-{}".format(s[2], s[1], s[0])     # convert to date Y-M-D
        dateSet.add(a)                              # compose set of dates, ADD - for sets
        subj["T"] = a
        subj["A"] = int(cols[1].text.strip())           # all, new covidints
        subj["D"] = int(cols[2].text.strip())           # dead
        subj["H"] = int(cols[3].text.strip())           # healed
        subj["I"] = int(cols[4].text.strip())           # still ill
        ee = '{}'.format(subj)
 #       print(ee)
        regda.append(subj)
        region = {"region": su["regName"], "regData": regda}
    print(su["regName"])
    bigData.append(region)

dateList = list(dateSet)
dateList.sort(reverse=True)


def regsort(x):
    if x['region'] == 'Вся Россия':
        return '_'
    return x['region']


bigData.sort(key=regsort)
rectangled = []
nullCovid = {'T': None, 'A': None, 'D': None, 'H': None, 'I': None}
for r in bigData:
    mass = []
    for i in range(len(dateList)):
        mass.append(nullCovid)
    for d in r['regData']:
        idx = dateList.index(d['T'])
        mass[idx] = d
    po = population[r['region']]
    rectangled.append({'region': r['region'], 'popula': po[0], 'ukol': po[1], 'regData': mass})

json_string = json.dumps(rectangled)
with open(dataFile, "w") as write_file:
    write_file.write(json_string)
with open('DATAS/lastCovid.json', "w") as write_file:
    write_file.write(json_string)


 #   json.dump(rectangled, write_file)
