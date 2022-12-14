# -*- coding: cp1251 -*
from bs4 import BeautifulSoup
import lxml
import requests
import wget
import urllib.request
import json
import os
import csv

population = {}
with open("WorldPopula.csv", encoding='utf-8') as r_file:
    reader = csv.reader(r_file, delimiter = ",")
    for row in reader:
        print(row)
        c = row[0]
        p = row[1]
        population[c] = p

dataFile = 'WOR.json'
dataFile = 'USAmidway.json'

with open(dataFile, "r") as read_file:
    data = json.load(read_file)

dateSet = set()

for r in data:
    for d in r['regData']:
        t = d['T']
        dateSet.add(t)

dateList = list(dateSet)
dateList.sort(reverse=True)


def regsort(x):
   return x['region']


#data.sort(key=regsort)
rectangled = []
nullCovid = {'T': None, 'A': None, 'D': None, 'H': None, 'I': None}
for r in data:
    mass = []
    for i in range(len(dateList)):
        nullCovid = {'T': dateList[i], 'A': None, 'D': None, 'H': None, 'I': None}
        mass.append(nullCovid)
    for d in r['regData']:
        idx = dateList.index(d['T'])
        mass[idx] = d
#    po = population[r["region"]]
#    rectangled.append({"region": r["region"], "popula": po, "regData": mass})

    po = data['population']
    rectangled.append({'region': r['region'], 'popula': po, 'tests': data['tests'],  'regData': mass})


#json_string = json.dumps(rectangled)
with open("woo1.json", "w") as write_file:
    json.dump(rectangled, write_file)



f = 9