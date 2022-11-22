import requests,time,cloudscraper,sqlite3,concurrent.futures,pandas as pd
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from rich import print 

MAX_THREADS = 30
db = "nadirkitap.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    #cur.execute("CREATE TABLE IF NOT EXISTS 'StockPrice' ('SKU' TEXT NOT NULL,'Date' DATE NOT NULL,'Stock' REAL NOT NULL,'Price' REAL NOT NULL,PRIMARY KEY('SKU','Date'));")
    #cur.execute("CREATE TABLE IF NOT EXISTS 'Products' ('SKU' TEXT,'Name' TEXT,'Categories' TEXT,'Size' REAL,'Unit' TEXT,'Material' TEXT,'Finish' TEXT,'Url' TEXT, 'CurrentPrice' REAL,'EstimatedSales' REAL,PRIMARY KEY('SKU'));")
    conn.commit()
    conn.close()

def insertAllBookLinks():
    #conn = sqlite3.connect(db)
    #cur = conn.cursor()
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    for i in range(0,1):
        books = f'https://www.nadirkitap.com/sitemap/kitap-{i}.txt'
        #print(books)
        data = scraper.get(books).text
        data=data.replace('\n',',')
        urls = data.split(',')
        i = 1
        for url in urls:
            print(i,url)
            i = i + 1
            #cur.execute("INSERT OR IGNORE INTO SiteMapLinks (URL) VALUES (?)",(url,))
    #conn.commit()
    #conn.close()

insertAllBookLinks()