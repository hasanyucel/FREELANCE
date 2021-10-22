import requests,time,cloudscraper,sqlite3,concurrent.futures,pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from rich import print 

MAX_THREADS = 30
db = "wallsandfloors.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'StockPrice' ('SKU' TEXT NOT NULL,'Date' DATE NOT NULL,'Stock'	REAL NOT NULL,'Price' REAL NOT NULL);")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Products' ('SKU' TEXT,'Name' TEXT,'Categories' TEXT,'Size' REAL,'Meas' TEXT,'Material' TEXT,'Finish' TEXT,'Url' TEXT,PRIMARY KEY('SKU'));")
    conn.commit()
    conn.close()

def insertAllSitemapLinks():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    xml = 'https://www.wallsandfloors.co.uk/sitemap.xml'
    r = requests.get(xml)
    soup = BeautifulSoup(r.text, 'lxml')
    urls = soup.find_all('url')
    for url in urls:
        pr = url.find('priority').text
        if pr == '1.0':
            stml = url.find('loc').text
            cur.execute("INSERT OR IGNORE INTO SiteMapLinks (URL) VALUES (?)",(stml,))
    conn.commit()
    conn.close()

def getSitemapLinks():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT Url FROM SiteMapLinks')
    links = cur.fetchall()
    links = [f[0] for f in links]
    conn.close()
    return links

def getProductInfo(url):
    print(url)
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=20)
    html = scraper.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    page_title = soup.title.text
    if page_title != "404 Not Found | Walls and Floors":
        specification = soup.find('table',attrs={'id':'product-attribute-specs-table'})
        sku = soup.find('td',attrs={'id':'product_id_web'}).text.strip()
        title = soup.find('h1',attrs={'class':'heading heading8 hidden-xs'}).text.strip()
        listAttributes = {}
        for tr in specification.findAll('tr'):
            listAttributes.update({tr.th.text.strip(): tr.th.find_next('td').text.strip()})
        if "Size" in listAttributes:
            size = listAttributes["Size"]
        else:
            size = "-"
        if "Sold By" in listAttributes:
            unit = listAttributes["Sold By"]
        else:
            unit = "-"
        if "Material type" in listAttributes:
            material = listAttributes["Material type"]
        else:
            material = "-"
        if "Finish" in listAttributes:
            finish = listAttributes["Finish"]
        else:
            finish = "-"
        price = soup.find('span',attrs={"class":"price"})
        if price is not None:
            price = price.text.strip()
            price = price.replace("£","")
        
        stock = soup.find('div', attrs={"class":"stock-due-date"}).text.strip()
        stock = stock.split(" ")
        stock = stock[0]
        print(sku,title,size,unit,material,finish,stock,price)
        time.sleep(0.25)


createDbAndTables()
insertAllSitemapLinks()
urls = getSitemapLinks()
for url in urls:
    getProductInfo(url)