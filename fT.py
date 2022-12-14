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

url = "https://gogov.ru/articles/covid-v-stats"
#url = "view-source:https://gogov.ru/articles/covid-v-stats"
response = requests.get(url,
            headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
str = response.text  # Access the HTML with the text property


#url = "rus.tab"
#with open(url, "r", encoding = 'utf-8') as fi:
#    str = fi.read()


s = BeautifulSoup(str, 'lxml')  # Parse the HTML as a string
regT = s.find('table', id="m-table")
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

#with open("rus1124Ukol.json", "w") as write_file:
 #   json.dump(data, write_file)
#with open("rus1124Ukol.json", "r") as read_file:
 #   vacc = json.load(read_file)

vacc = data

popu = {}

for r in population:
    p = r.replace('область', "")
    p = p.replace('край', "")
    p = p.replace('Республика', "")
    p = p.replace('республика', "").strip()
    p = p.replace('автономная', "").strip()
    p = p.replace('автономный округ', "").strip()
    popu[r] = [p, population[r], 0]


for r in popu:
    cmp = ""
    p = popu[r][0]
    for v in vacc:
        if len(p) < len(v['regName']) :
            b = p
        else:
            b = v['regName']
        c = len(b)
        if ( p[0:c] == v['regName'][0:c]):
            popu[r][2] = v['privProc']
            popu[r][0] = v['regName']
            cmp = v['regName']
            break
    if cmp == '':
        if p != "Вся Россия":
            lng = len(p)
            while (lng > 0) and (cmp ==""):
                for v in vacc:
                    if (p[0:lng] == v['regName'][0:lng]):
                        popu[r][2] = v['privProc']
                        popu[r][0] = v['regName']
                        cmp = v['regName']
                        break
                lng = lng - 1
        else:
            popu[r][2] = 50.1
            popu[r][0] = "Россия"
            cmp = v['regName']



with open("urusas.py", "w") as write_file:
    write_file.write("# -*- coding: cp1251 -*\n")
    write_file.write("population = {\n")
    for r in popu:
        a = popu[r]
        ee = '"{}":\t[{}, {}], \n'.format(r, a[1], a[2])
        print(ee)
        write_file.write(ee)
    write_file.write('}\n')
