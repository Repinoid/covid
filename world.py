# -*- coding: cp1251 -*
from bs4 import BeautifulSoup
import lxml
import requests
import wget
import urllib.request
import json
import os
import csv
#from pops import population

population = {}
with open("WorldPopula.csv", encoding='utf-8') as r_file:
    reader = csv.reader(r_file, delimiter = ",")
    for row in reader:
        print(row)
        population[row[0]] = row[1]


#exit()

url = "https://russian-trade.com/coronavirus-russia/moskva/"
response = requests.get(url)
txt = response.text  # Access the HTML with the text property
soup = BeautifulSoup(txt, 'lxml')  # Parse the HTML as a string
regT = soup.find('table', id='curs_special')
rows = regT.find_all('tr')
rowLastDat = rows[1]
cols = rowLastDat.find_all('td')
lastDat = cols[0].text.strip()
dataFile = 'DATAS/World_' + lastDat + ".json"
#if os.path.isfile(dataFile):
 #   exit()                  # stop if last date already exists

url = 'https://russian-trade.com/coronavirus/'
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
    shi = 0
    subj = {}
    if cols[0].has_attr('colspan'):        # if no first cell
        shi = 1
        subj["regName"]     =       "ВЕСЬ МИР"
    else:
        subj["regName"]     =       cols[1-shi].text.strip()
    hre = cols[1-shi].find('a')
    if ( hre == None):
        continue ;
    if (  hre.has_attr('href') == False ):
        continue
    subj["ref2"]        =       cols[1-shi].find('a').get('href')
    subj["allZ"]        =       cols[2-shi].text.strip().partition('(')[0]
    subj["trup"]        =       cols[3-shi].text.strip().partition('(')[0]
    subj["heal"]        =       cols[4-shi].text.strip().partition('(')[0]
    subj["zaraza"]      =       cols[5-shi].text.strip().partition('(')[0]
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
    if x['region'] == 'ВЕСЬ МИР':
        return '_'
    return x['region']

json_string = json.dumps(bigData)
with open('WOR.json', "w") as write_file:
    write_file.write(json_string)

bigData.sort(key=regsort)
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
    if (r['region'] in population ):
        po = population[r['region']]
        rectangled.append({'region': r['region'], 'popula': po,   'regData': mass})

json_string = json.dumps(rectangled)
with open(dataFile, "w") as write_file:
    write_file.write(json_string)
with open('DATAS/lastWorld.json', "w") as write_file:
    write_file.write(json_string)


 #   json.dump(rectangled, write_file)
