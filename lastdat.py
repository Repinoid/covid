import requests
import re

url = "https://russian-trade.com/coronavirus-russia/moskva/"
response = requests.get(url)
txt = response.text  # Access the HTML with the text property

patter = '<table\s+id="curs_special".+<tr><td>\d{2}.\d{2}.\d{4}</td>'
lastDataCell = "<tr><td>\d{2}.\d{2}.\d{4}</td>"

tabloidPosition = re.search(patter, txt).regs[0][0]
lastDataCellPosition = re.search(lastDataCell, txt[tabloidPosition:])
lastDatBeg = tabloidPosition+lastDataCellPosition.regs[0][0] + len('<tr><td>')
lastDatEnd = tabloidPosition+lastDataCellPosition.regs[0][1] - len('</td>')
cus = txt[lastDatBeg:lastDatEnd]
datta = f"{cus[6:10]}-{cus[3:5]}-{cus[0:2]}"

print (datta)