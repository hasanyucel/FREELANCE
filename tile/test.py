import requests,time,cloudscraper,sqlite3,concurrent.futures
from bs4 import BeautifulSoup
from rich import print 

MAX_THREADS = 30
products = []

def createDbAndTables():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXIST 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    cur.execute("CREATE TABLE IF NOT EXIST 'StockPrice' ('SKU' TEXT NOT NULL,'Date' DATE NOT NULL,'Stock'	REAL NOT NULL,'Price' REAL NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXIST 'Products' ('SKU' TEXT,'Name' TEXT,'Size' REAL,'Meas' TEXT,'Finish' TEXT,'Url' TEXT);")
    conn.close()

def getAllLinks():
    xml = 'https://www.tilemountain.co.uk/sitemap/sitemap.xml'
    r = requests.get(xml)
    soup = BeautifulSoup(r.text, 'lxml')
    urls = [loc.string for loc in soup.find_all('loc')]
    with open("links.txt", "a") as fh:
        for url in urls:
            if url.startswith("https://www.tilemountain.co.uk/p/"):
                fh.write(url+"\n")

def product_info(url):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    html = scraper.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    print(url)
    sku = soup.find('span',attrs={"class":"sku-value"}).text.strip()
    title = soup.find('h1',attrs={"class":"mb20 mt0 cl-mine-shaft product-name"}).text.strip()
    size = soup.find('span',attrs={"class":"size-value"})
    if size is not None:
        size = size.text
    else:
        size = None
    stock = soup.find('span',attrs={"class":"sqm"}).text
    price = soup.find('span',attrs={"class":"h2 cl-mine-shaft weight-700"}).text.strip()
    metarial = soup.select("#viewport > div.product-page-detail > section.container.px15.pt20.pb35.cl-accent.details.product-desc > div > div > div.col-xs-12.col-sm-12.col-md-12.col-lg-6.infoprod-col > div > div.tabs-content-box > div > div > ul > li:nth-child(8) > span.detail")
    if metarial:
        metarial = metarial[0].text
    else:
        metarial = "-"

    product = (sku,title,size,metarial,stock,price,url)
    print(product)
    products.append(product)
    time.sleep(0.25)
    
def PoolExecutor(urls):
    threads = min(MAX_THREADS, len(urls))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(product_info, urls)

#getAllLinks() sitemap.xml deki product linklerini çeker
urls = []
f = open("links.txt",'r') 
for line in f:
    line = line.replace("\n", "")
    urls.append(line)
    #product_info(line)

t0 = time.time()
PoolExecutor(urls)
t1 = time.time()
print(len(urls),len(products))
print(f"{t1-t0} seconds.")
#product_info("https://www.tilemountain.co.uk/p/lounge-light-grey-polished-porcelain-885.html")