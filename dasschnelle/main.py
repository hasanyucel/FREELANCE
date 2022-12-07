import cloudscraper,pandas,time,sqlite3,json
from rich import print
from bs4 import BeautifulSoup
from bs2json import bs2json


db = "dasschnelle.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    conn.commit()

def insertAllLinks(xml,table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    r = scraper.get(xml)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text, 'lxml')
    urls = [loc.string for loc in soup.find_all('loc')]
    for url in urls:
        cur.execute(f"INSERT OR IGNORE INTO {table_name} (URL) VALUES (?)",(url,))
    conn.commit()
    conn.close()

def getTableColumn(table_name,column_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f'SELECT {column_name} FROM {table_name}')
    links = cur.fetchall()
    links = [f[0] for f in links]
    conn.close()
    return links

def getIdentityDetails(link):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    r = scraper.get(link)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text,'lxml')
    json_tag = soup.find_all('script',attrs={'type':'application/ld+json'})
    
    converter = bs2json()
    json_ = converter.convertAll(json_tag,join=True)
    data = json_[0]['script'][-1]['text']
    json_object = json.loads(data)

    name = json_object["name"]
    description = json_object["description"]

    streetAddress = json_object["address"]["streetAddress"]
    postalCode = json_object["address"]["postalCode"]
    addressLocality = json_object["address"]["addressLocality"]
    addressRegion = json_object["address"]["addressRegion"]
    addressCountry = json_object["address"]["addressCountry"]
    latitude = json_object["geo"]["latitude"]
    longitude = json_object["geo"]["longitude"]

    telephones = json_object["telephone"]
    email = json_object["email"]
    urls = json_object["url"]

    logo = json_object["logo"]
    images = json_object["image"]
    priceRange = json_object["priceRange"]
    print(description)


print("Script is working...")
t0 = time.time()
#createDbAndTables()
#insert sitemap link https://www.dasschnelle.at/sitemaps/dasschnelle-at/detail_sitemap_customers-1.xml
#insert sitemap link https://www.dasschnelle.at/sitemaps/dasschnelle-at/detail_sitemap_customers-2.xml

#urls = getTableColumn('SiteMapLinks','Url')
#for url in urls: 
#    insertAllLinks(url,'SiteLinks')

#urls = getTableColumn('SiteLinks','Url')
#for url in urls:
#    getIdentityDetails(url)

getIdentityDetails('https://www.dasschnelle.at/schatz-christian-imst-stadtplatz')

t1 = time.time()
print(f"{t1-t0} seconds.")