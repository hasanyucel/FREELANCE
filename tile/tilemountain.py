import requests,time,cloudscraper,sqlite3,concurrent.futures,pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from rich import print 

MAX_THREADS = 30
db = "tilemountain.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'StockPrice' ('SKU' TEXT NOT NULL,'Date' DATE NOT NULL,'Stock'	REAL NOT NULL,'Price' REAL NOT NULL);")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Products' ('SKU' TEXT,'Name' TEXT,'Categories' TEXT,'Size' REAL,'Unit' TEXT,'Material' TEXT,'Finish' TEXT,'Url' TEXT,PRIMARY KEY('SKU'));")
    conn.commit()
    conn.close()

def insertAllSitemapLinks():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    xml = 'https://www.tilemountain.co.uk/sitemap/sitemap.xml'
    r = requests.get(xml)
    soup = BeautifulSoup(r.text, 'lxml')
    urls = [loc.string for loc in soup.find_all('loc')]
    for url in urls:
        if url.startswith("https://www.tilemountain.co.uk/p/"):
            cur.execute("INSERT OR IGNORE INTO SiteMapLinks (URL) VALUES (?)",(url,))
    conn.commit()
    conn.close()

def getProductInfo(url):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    html = scraper.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    sku = soup.find('span',attrs={"class":"sku-value"}).text
    sku = sku.replace("SKU:","").strip()
    title = soup.find('h1',attrs={"class":"mb20 mt0 cl-mine-shaft product-name"}).text.strip()
    size = soup.find('span',attrs={"class":"size-value"})
    if size is not None:
        size = size.text
        size = size.replace("Size","")
        size = size.strip()
    else:
        size = "No Size Info"
    unit = soup.find('span',attrs={"class":"sqm-title-special"})
    if unit is not None:
        unit = unit.text
        unit = unit.replace("/","").strip()
    else:
        unit = soup.find('span',attrs={"class":"sqm-title"}).text
        unit = unit.replace("/","").strip()
    if unit == "inc VAT":
        unit = soup.find('label', attrs={"class":"sqm-txt"}).text
        unit = unit.replace("/","").strip()
    stock = soup.find('span', attrs={"class":"sqm"}).text 
    if stock.startswith("In") or stock.startswith("Out") or stock.startswith("More"):
        stock = stock + ""
    else:
        stock = stock.split(" ")
        stock = stock[0]
    price = soup.find('span',attrs={"class":"specialprice"})
    if price is not None:
        price = price.text.strip()
    else:
        price = soup.find('span',attrs={"class":"h2 cl-mine-shaft weight-700"}).text.strip()
    price = price.replace("£","")
    attributes = soup.find('ul',attrs={"class":"attributes productDetails"})
    listAttributes = {}
    for li in attributes.findAll('li'):
        listAttributes.update({li.span.text.strip(): li.span.find_next('span').text.strip()})
    if "Material" in listAttributes:
        material = listAttributes["Material"]
    else:
        material = "-"
    if "Finish" in listAttributes:
        finish = listAttributes["Finish"]
    else:
        finish = "-"
    category = soup.find('div',attrs={"class":"breadcrumbs h5 cl-gray pt40 pb20 hidden-xs breadcrumb"})
    category = category.findAll('a')
    categories = []
    for x in category:
        categories.append(x.text.strip())
    categories = '/'.join(categories)
    insertProductInfos(sku,title,categories,size,unit,material,finish,url) 
    date = datetime.today().strftime("%d/%m/%Y")
    insertProductStockPrice(sku, date, stock, price)
    time.sleep(0.25)
    print(sku,title,categories,size,unit,material,finish,stock,price,url)
    
def insertProductInfos(sku,name,categories,size,unit,material,finish,url):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO Products (sku,name,categories,size,unit,material,finish,url) VALUES (?,?,?,?,?,?,?,?)",(sku,name,categories,size,unit,material,finish,url))
    conn.commit()
    conn.close()

def insertProductStockPrice(sku,date,stock,price):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("INSERT INTO StockPrice (sku,date,stock,price) VALUES (?,?,?,?)",(sku,date,stock,price))
    conn.commit()
    conn.close()

def PoolExecutor(urls):
    threads = min(MAX_THREADS, len(urls))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(getProductInfo, urls)

def getSitemapLinks():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT Url FROM SiteMapLinks')
    links = cur.fetchall()
    links = [f[0] for f in links]
    conn.close()
    return links

def getPivotStockPrice():
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("select distinct p.url,p.sku,p.name,p.size,p.unit,p.material,p.finish,s.date,s.stock,s.price from products p join stockprice s on p.sku = s.sku order by p.categories", conn)
    df1 = df.pivot_table(index =['Url','SKU','Name','Size','Unit','Material','Finish'], columns ='Date', values ='Price',aggfunc='first')
    df2 = df.pivot_table(index =['Url','SKU','Name','Size','Unit','Material','Finish'], columns ='Date', values ='Stock',aggfunc='first')
    #df1 = df.swaplevel(0,1, axis=1).sort_index(axis=1)
    #df.columns = df.columns.swaplevel(0, 1)
    #df.sort_index(axis=1, level=0, inplace=True)
    #print(df)
    writer = pd.ExcelWriter('tilemountain.xlsx')
    df1.to_excel(writer,sheet_name ='Price')  
    df2.to_excel(writer,sheet_name ='Stock')  
    writer.save()
    conn.close()

def getLicenceDate():
    licence_key = ""
    link = "https://drive.google.com/file/d/1bZ87-1f2WRU5i0etRLAYRIbaPXax1dz4/view?usp=sharing"
    with open('licence.txt') as f:
        licence_key = f.readline().strip()
    file_id=link.split('/')[-2]
    dwn_url='https://drive.google.com/uc?id=' + file_id
    df = pd.read_csv(dwn_url)
    row = df.query('account == "tilemountain" & key == "'+licence_key+'"')
    tarih = row["tarih"].values[0]
    return tarih

today = datetime.today().strftime("%d/%m/%Y")
licence = getLicenceDate()
if(today < licence):
    print("Script is working...")
    t0 = time.time()
    createDbAndTables()
    insertAllSitemapLinks()
    urls = getSitemapLinks()
    """for url in urls:
        getProductInfo(url)"""
    PoolExecutor(urls)#Hatalar alınmıyor. Manuel test et."""
    getPivotStockPrice()
    t1 = time.time()
    print(f"{t1-t0} seconds.")
else:
    print("Trial time has been finished.")