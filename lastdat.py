import requests
import re
from bs4 import BeautifulSoup

# получить дату последней статистики по ковиду - из таблицы по Москве (по умолчанию)
def getLastCodidDate(url = "https://russian-trade.com/coronavirus-russia/moskva/"):
    response = requests.get(url)
    txt = response.text                                                     # Access the HTML with the text property
    patter = '<table\s+id="curs_special".+<tr><td>\d{2}.\d{2}.\d{4}</td>'
    lastDateCell = "<tr><td>\d{2}.\d{2}.\d{4}</td>"                         # pattern dd?mm?yyyy
    tabloidPosition = re.search(patter, txt).regs[0][0]                     # ищем начало таблицы by patter regex
    lastDataCellPosition = re.search(lastDateCell, txt[tabloidPosition:])   # ищем дату начиная от начала таблицы
    lastDatBeg = tabloidPosition+lastDataCellPosition.regs[0][0] + len('<tr><td>')  # начало ячейки и датой
    lastDatEnd = tabloidPosition+lastDataCellPosition.regs[0][1] - len('</td>')     # конец
    cus = txt[lastDatBeg:lastDatEnd]                                                # вырезаем кусок с датой
    dateS = {}                              # словарь для даты
    try:
        dateS["Year"]   = int(cus[6:10])    # из формата dd.mm.yyyy
        dateS["Month"]  = int(cus[3:5])
        dateS["Day"]    = int(cus[0:2])
    except ValueError:
        dateS = None
    return dateS

def getRusRegionsList(url = 'https://russian-trade.com/coronavirus-russia/') :
    response = requests.get(url)
    txt = response.text                             # Access the HTML with the text property
    soup = BeautifulSoup(txt, 'lxml')               # Parse the HTML as a string
    regT = soup.find('table', id='curs_special')    # find the table
    rows = regT.find_all('tr')                      # get rows list
    regas = []              # list for regions
    for row in rows:
        cells = row.find_all('td')                  # get cells in the row
        if ( not len(cells) ):                      # if no 'TD' cells - 'TH' in the header
            continue
        subj = {}           # dict region name: URL
        subj["regName"]     =       cells[1].text.strip()           # second cell - region name
        subj["ref2"]        =       cells[1].find('a').get('href')  # third cell - link to region page
        regas.append(subj)
    return (regas)

a = getRusRegionsList()
print(a)

