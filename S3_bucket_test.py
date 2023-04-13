# -*- coding: cp1251 -*
import boto3
import lxml
import requests
import urllib.request
import requests
import re
import json
from bs4 import BeautifulSoup
from urusas import population





from dostup import keys

# получить дату последней статистики по ковиду - из таблицы по Москве (по умолчанию)
def getLastCodidDate(url="https://russian-trade.com/coronavirus-russia/moskva/"):
    response = requests.get(url)
    # Access the HTML with the text property
    txt = response.text
    patter = '<table\s+id="curs_special".+<tr><td>\d{2}.\d{2}.\d{4}</td>'
    # pattern dd?mm?yyyy
    lastDateCell = "<tr><td>\d{2}.\d{2}.\d{4}</td>"
    # ищем начало таблицы by patter regex
    tabloidPosition = re.search(patter, txt).regs[0][0]
    # ищем дату начиная от начала таблицы
    lastDataCellPosition = re.search(lastDateCell, txt[tabloidPosition:])
    # начало ячейки и датой
    lastDatBeg = tabloidPosition + \
        lastDataCellPosition.regs[0][0] + len('<tr><td>')
    lastDatEnd = tabloidPosition + \
        lastDataCellPosition.regs[0][1] - len('</td>')     # конец
    # вырезаем кусок с датой
    cus = txt[lastDatBeg:lastDatEnd]
    dateS = {}                              # словарь для даты
    try:
        dateS["Year"] = int(cus[6:10])    # из формата dd.mm.yyyy
        dateS["Month"] = int(cus[3:5])
        dateS["Day"] = int(cus[0:2])
    except ValueError:
        dateS = None
    return dateS


def getRusRegionsList(url='https://russian-trade.com/coronavirus-russia/'):
    response = requests.get(url)
    # Access the HTML with the text property
    txt = response.text
    # Parse the HTML as a string
    soup = BeautifulSoup(txt, 'lxml')
    regT = soup.find('table', id='curs_special')    # find the table
    rows = regT.find_all('tr')                      # get rows list
    regas = []              # list for regions
    for row in rows:
        cells = row.find_all('td')                  # get cells in the row
        if (not len(cells)):                      # if no 'TD' cells - 'TH' in the header
            continue
        subj = {}           # dict region name: URL
        # second cell - region name
        subj["regName"] = cells[1].text.strip()
        subj["ref2"] = cells[1].find('a').get(
            'href')  # third cell - link to region page
        regas.append(subj)
    return (regas)


def getRegionCovidData(regURL):
    region_data = []
    ref = "https://russian-trade.com/coronavirus-russia/" + regURL
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(ref, headers=headers, stream=True)
    if (response.status_code != 200):
        return None
    txt = response.text  # Access the HTML with the text property
    al = len(txt)
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

def write2bucket(event, context):
    session = boto3.session.Session()
    client = session.client(
        service_name='s3',
        endpoint_url        =   keys['endpoint_url'],
   #     aws_access_key_id=os.getenv("aws_access_key_id"),
   #     aws_secret_access_key=os.getenv('aws_secret_access_key'),
   #     region_name=os.getenv('region_name'),
        aws_access_key_id=keys['aws_access_key_id'],
        aws_secret_access_key=keys['aws_secret_access_key'],
        region_name=keys['region_name'],
    )
    Body = bytes(json.dumps(event["data"], indent=2).encode('UTF-8'))
    response = client.put_object(
        Body=Body,
        Bucket='covitus',
        Key= f'russia/{event["region"]}.json',
    )
    return response

region = "moskva"
dt = getRegionCovidData(region)
eventus = {"data": dt, "region": region}

resp = write2bucket(eventus, 0)

f = 8
