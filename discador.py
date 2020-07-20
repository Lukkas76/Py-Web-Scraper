import requests
from bs4 import BeautifulSoup
import csv
import re
import pyodbc

server = 'sql-math-santander.database.windows.net'
database = 'DB_Sherlock'
username = 'sasantander'
password = 'S@nt@3@564'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

r = requests.get('https://www.santander.com.br/sitemap.xml')
xml = r.text

soup = BeautifulSoup(xml, features="xml")
element = soup.find_all('loc')
for w in range(len(element)):
    lista = str(element[w]).replace('<loc>','').replace('</loc>', '')
    pages_snt = [lista]
    print(pages_snt)
    for pg in pages_snt:
        page = requests.get(pg)
        soup = BeautifulSoup(page.text, 'html.parser')
        [x.extract() for x in soup.findAll('script')]
        insideBody = soup.find_all('body')
        print(insideBody)
        sqlCommand = "INSERT INTO Sitemap_content (txt_HTML, txt_URL) VALUES (?, ?)"
        cursor.execute(sqlCommand, str(insideBody).replace('[','').replace(']',''), str(pages_snt).replace('[','').replace(']',''))
        cnxn.commit()







    # teste = soup.findAll(text=re.compile("IOF"))
    # if teste != []:
    #     teste = "Sim"
    # else:
    #     teste = "Não"
    # wtr = csv.writer(open('IOF.csv', 'a'), delimiter=',', lineterminator='\n')
    # wtr.writerow([teste, pg])

print('done')