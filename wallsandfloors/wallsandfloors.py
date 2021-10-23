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
    cur.execute("CREATE TABLE IF NOT EXISTS 'StockPrice' ('SKU' TEXT NOT NULL,'Date' DATE NOT NULL,'Stock' REAL NOT NULL,'Price' REAL NOT NULL,PRIMARY KEY('SKU','Date'));")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Products' ('SKU' TEXT,'Name' TEXT,'Categories' TEXT,'Size' REAL,'Unit' TEXT,'Material' TEXT,'Finish' TEXT,'Url' TEXT, 'CurrentPrice' REAL,'EstimatedSales' REAL,PRIMARY KEY('SKU'));")
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
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=20)
    html = scraper.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    page_title = soup.title.text
    if page_title.startswith("404 Not Found") == False:
        page_type = soup.find("meta", property="og:type")
        if page_type is not None:
            page_type = page_type['content']
            if page_type == 'product':
                listAttributes = {}
                time.sleep(0.25)
                specification = soup.find('section',attrs={'class':'block component-waf-accordion -xs'})
                if specification is not None:
                    for tr in specification.find_all('tr'):
                        listAttributes.update({tr.th.text.strip(): tr.th.find_next('td').text.strip()})
                    if "Sku" in listAttributes:
                        sku = listAttributes["Sku"]
                    else:
                        sku = "-"
                    title = soup.find('h1',attrs={'class':'heading heading8 hidden-xs'}).text.strip()
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
                    if stock.startswith("In") or stock.startswith("Out"):
                        stock = stock + ""
                    else:
                        stock = stock.split(" ")
                        stock = stock[0]
                    print(sku,title,size,unit,material,finish,stock,price)
                    insertProductInfos(sku,title,"",size,unit,material,finish,url,price) 
                    date = datetime.today().strftime("%d/%m/%Y")
                    insertProductStockPrice(sku, date, stock, price)
        
def insertProductInfos(sku,name,categories,size,unit,material,finish,url,currentprice):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO Products (sku,name,categories,size,unit,material,finish,url,currentprice) VALUES (?,?,?,?,?,?,?,?,?)",(sku,name,categories,size,unit,material,finish,url,currentprice))
    conn.commit()
    conn.close()

def insertProductStockPrice(sku,date,stock,price):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO StockPrice (sku,date,stock,price) VALUES (?,?,?,?)",(sku,date,stock,price))
    conn.commit()
    conn.close()

def PoolExecutor(urls):
    threads = min(MAX_THREADS, len(urls))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(getProductInfo, urls)

def calculateEstimatedSales():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT distinct sku FROM Products')
    products = cur.fetchall()
    print("Estimated Sales is calculating...")
    for row in products:
        sku = row[0]
        cur.execute(f'select sum(Difference)from (SELECT stock - LAG(stock) OVER (ORDER BY Date) AS Difference FROM StockPrice where sku="{sku}")')
        dif = cur.fetchone()
        dif = dif[0]
        if dif is None:
            dif = 0
        if dif <= 0:
            updateEstimatedSales(sku,dif)
        else:
            updateEstimatedSales(sku, 0)   
    conn.close()

def updateEstimatedSales(sku,dif):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f'UPDATE Products SET EstimatedSales = "{dif}" WHERE sku = "{sku}";')
    conn.commit()
    conn.close()

def makeHyperlink(url):
    return f'=Hyperlink("{url}","Product")'

def getPivotStockPrice():
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("select distinct p.url,p.sku,p.name,p.size,p.unit,p.material,p.finish,p.currentprice,p.estimatedsales,s.date,s.stock,s.price from products p join stockprice s on p.sku = s.sku order by p.categories", conn)
    df = pd.DataFrame(df)
    df['Url'] = df.apply(lambda row : makeHyperlink(row['Url']), axis = 1)
    df1 = df.pivot_table(index =['Url','SKU','Name','Size','CurrentPrice','EstimatedSales','Unit','Material','Finish'], columns ='Date', values ='Price',aggfunc='first')
    df2 = df.pivot_table(index =['Url','SKU','Name','Size','CurrentPrice','EstimatedSales','Unit','Material','Finish'], columns ='Date', values ='Stock',aggfunc='first')
    df1 = df1.sort_values("EstimatedSales")
    df2 = df2.sort_values("EstimatedSales")
    writer = pd.ExcelWriter('wallsandfloors.xlsx')
    df1.to_excel(writer,sheet_name ='Price')  
    df2.to_excel(writer,sheet_name ='Stock')  
    writer.save()
    conn.close()

print("Script is working...")
t0 = time.time()
createDbAndTables()
insertAllSitemapLinks()
urls = getSitemapLinks()
"""for url in urls:
    getProductInfo(url)"""
PoolExecutor(urls)#Hatalar alınmıyor. Manuel test et."""
calculateEstimatedSales()
getPivotStockPrice()
t1 = time.time()
print(f"{t1-t0} seconds.")

import sys
def check_quit(inp):
    if inp == 'q':
        sys.exit(0)
x = str(input("Please press 'q' to exit: "))
check_quit(x)