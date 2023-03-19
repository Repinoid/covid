import requests
import re

def getLastCodidDate(url = "https://russian-trade.com/coronavirus-russia/moskva/"):

    response = requests.get(url)
    txt = response.text  # Access the HTML with the text property

    patter = '<table\s+id="curs_special".+<tr><td>\d{2}.\d{2}.\d{4}</td>'
    lastDateCell = "<tr><td>\d{2}.\d{2}.\d{4}</td>"

    tabloidPosition = re.search(patter, txt).regs[0][0]
    lastDataCellPosition = re.search(lastDateCell, txt[tabloidPosition:])
    lastDatBeg = tabloidPosition+lastDataCellPosition.regs[0][0] + len('<tr><td>')
    lastDatEnd = tabloidPosition+lastDataCellPosition.regs[0][1] - len('</td>')
    cus = txt[lastDatBeg:lastDatEnd]
    dateS = {}
    try:
        dateS["Year"]   = int(cus[6:10])
        dateS["Month"]  = int(cus[3:5])
        dateS["Day"]    = int(cus[0:2])
    except ValueError:
        dateS = None
    return dateS

