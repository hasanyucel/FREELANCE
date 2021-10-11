import requests,time,cloudscraper,sqlite3,concurrent.futures
from datetime import datetime
from bs4 import BeautifulSoup
from rich import print 

MAX_THREADS = 30

def createDbAndTables():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'StockPrice' ('SKU' TEXT NOT NULL,'Date' DATE NOT NULL,'Stock'	REAL NOT NULL,'Price' REAL NOT NULL);")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Products' ('SKU' TEXT,'Name' TEXT,'Categories' TEXT,'Size' REAL,'Meas' TEXT,'Material' TEXT,'Finish' TEXT,'Url' TEXT,PRIMARY KEY('SKU'));")
    conn.commit()
    conn.close()

def insertAllSitemapLinks():
    conn = sqlite3.connect('db.sqlite')
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
    print(url)
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
    meas = soup.find('span',attrs={"class":"sqm-title-special"})
    if meas is not None:
        meas = meas.text
        meas = meas.replace("/","").strip()
    else:
        meas = soup.find('span',attrs={"class":"sqm-title"}).text
        meas = meas.replace("/","").strip()
    if meas == "inc VAT":
        meas = soup.find('label', attrs={"class":"sqm-txt"}).text
        meas = meas.replace("/","").strip()
    

    stock = soup.find('span', attrs={"class":"sqm"}).text #STARTSWITH KULLAN
    if stock == "In Stock":
        stock = "In Stock"
    elif stock == "Out Of Stock ":
        stock = "Out Of Stock"
    elif stock == "More Stock":
        stock = "More Stock"
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
        material = "No Material Info"
    if "Finish" in listAttributes:
        finish = listAttributes["Finish"]
    else:
        finish = "No finish Info"
    category = soup.find('div',attrs={"class":"breadcrumbs h5 cl-gray pt40 pb20 hidden-xs breadcrumb"})
    category = category.findAll('a')
    categories = []
    for x in category:
        categories.append(x.text.strip())
    categories = '/'.join(categories)
    insertProductInfos(sku,title,categories,size,meas,material,finish,url) 
    date = datetime.today().strftime("%d/%m/%Y")
    insertProductStockPrice(sku, date, stock, price)
    time.sleep(0.25)
    #print(sku,title,categories,size,meas,material,finish,url)
    print(sku, date, stock, price)
    
def insertProductInfos(sku,name,categories,size,meas,material,finish,url):
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO Products (sku,name,categories,size,meas,material,finish,url) VALUES (?,?,?,?,?,?,?,?)",(sku,name,categories,size,meas,material,finish,url))
    conn.commit()
    conn.close()

def insertProductStockPrice(sku,date,stock,price):
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute("INSERT INTO StockPrice (sku,date,stock,price) VALUES (?,?,?,?)",(sku,date,stock,price))
    conn.commit()
    conn.close()

def PoolExecutor(urls):
    threads = min(MAX_THREADS, len(urls))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(getProductInfo, urls)

def getSitemapLinks():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT Url FROM SiteMapLinks')
    links = cur.fetchall()
    links = [f[0] for f in links]
    conn.close()
    return links


t0 = time.time()
createDbAndTables()
insertAllSitemapLinks()
urls = getSitemapLinks()
#PoolExecutor(urls)#Hatalar alınmıyor. Manuel test et.
for url in urls:
    getProductInfo(url)
t1 = time.time()
print(f"{t1-t0} seconds.")

#getProductInfo("https://www.tilemountain.co.uk/p/surface-mid-grey-lapatto-wall-and-floor-tile.html")
#Date parametresini düzelt.
#Stock değişkenini doğru çek
#Price bilgisini kontrol et. Sale olabilir!