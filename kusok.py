# -*- coding: cp1251 -*
from bs4 import BeautifulSoup
import lxml
import requests
import wget
import urllib.request
import json
import os
from pops import population

a = population['Ульяновская область']

dataFile = 'DATAS/16.10.2021.json'

with open(dataFile, "r") as read_file:
    data = json.load(read_file)

dateSet = set()

for r in data:
    for d in r['regData']:
        t = d['T']
        s = t.split('.')
        a = "{}-{}-{}".format(s[2], s[1], s[0])
        d['T'] = a
        dateSet.add(a)

dateList = list(dateSet)
dateList.sort(reverse=True)


def regsort(x):
    if x['region'] == 'Вся Россия':
        return '_'
    return x['region']


data.sort(key=regsort)
rectangled = []
nullCovid = {'T': None, 'A': None, 'D': None, 'H': None, 'I': None}
for r in data:
    mass = []
    for i in range(len(dateList)):
        mass.append(nullCovid)
    for d in r['regData']:
        idx = dateList.index(d['T'])
        mass[idx] = d
    po = population[r['region']]
    rectangled.append({'region': r['region'], 'popula': po, 'regData': mass})

#json_string = json.dumps(rectangled)
with open("aaa.json", "w") as write_file:
    json.dump(rectangled, write_file)



f = 9