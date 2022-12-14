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


with open("rus1124Ukol.json", "r") as read_file:
    vacc = json.load(read_file)

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



with open("urusas1124.py", "w") as write_file:
    write_file.write("# -*- coding: cp1251 -*\n")
    write_file.write("population = {\n")
    for r in popu:
        a = popu[r]
        ee = '"{}":\t[{}, {}], \n'.format(r, a[1], a[2])
        print(ee)
        write_file.write(ee)
    write_file.write('}\n')
