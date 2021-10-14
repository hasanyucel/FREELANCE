import requests,sqlite3,cloudscraper
from bs4 import BeautifulSoup
from rich import print

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

"""createDbAndTables()
insertAllSitemapLinks()
urls = getSitemapLinks()
print(urls)"""

url = "https://www.wallsandfloors.co.uk/flat-covent-garden-pink-gloss-200x100-tiles/"
scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
html = scraper.get(url).content
soup = BeautifulSoup(html, 'lxml')
sku = soup.find('td',attrs={'id':'product_id_web'}).text
name = soup.find('h1',attrs={'class':'heading heading8 hidden-xs'}).text
categories = soup.find('ul',attrs={'class':'list-inline f14'})
categories = categories.find_all('span',attrs={'itemprop':'name'})
category = []
for x in categories:
    category.append(x.text.strip())
category = '/'.join(category)

print(category)