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
from pops import population

popul = {}
with open("WorldPopula.csv", encoding='utf-8') as r_file:
    reader = csv.reader(r_file, delimiter = ",")
    for row in reader:
        popul[row[0].lower()] = row[1]

with open("worldUkolot.json", "r") as read_file:
    vacc = json.load(read_file)

wvacin = {}
with open("wv.csv", "w") as r_file:
    for row in vacc:
        wvacin[row['regName'].lower()] = row['privProc']
        a = '{},{}\n'.format(row['regName'].lower(),row['privProc'])

for row in vacc:
    wvacin[row['regName'].lower()] = row['privProc']

w1 = set(popul.keys())
w2 = set(wvacin.keys())
w3 = w1.intersection(w2)

with open("DATAS/lastWorld.json", "r") as read_file:
    wor = json.load(read_file)

mas = []
for p in wor:
    reg = p['region'].lower()
    if reg in wvacin:
        v = wvacin[reg]
        i = 0
        while p['regData'][i]['A'] == None:
            i = i + 1
        rd = p['regData'][i]
        po = int(p['popula'])/1000000
        dat = {'region':  p['region'], 'V': v, 'A': int(rd['A']/po), 'D': int(rd['D']/po) }
        mas.append(dat)

json_string = json.dumps(mas)
with open("worldVa.json", "w") as write_file:
    write_file.write(json_string)

a = 6