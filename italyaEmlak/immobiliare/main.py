import requests,time,sqlite3,concurrent.futures
from bs4 import BeautifulSoup

db = "immobiliare.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    conn.commit()

def insertAllLinks(xml,table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    r = requests.get(xml)
    soup = BeautifulSoup(r.text, 'lxml')
    urls = [loc.string for loc in soup.find_all('loc')]
    for url in urls:
        cur.execute(f"INSERT OR IGNORE INTO {table_name} (URL) VALUES (?)",(url,))
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

print("Script is working...")
t0 = time.time()
createDbAndTables()
insertAllLinks('https://www.immobiliare.it/sitemap.xml','SiteMapLinks')
urls = getSitemapLinks()
for url in urls:
    insertAllLinks(url,'SiteLinks')

t1 = time.time()
print(f"{t1-t0} seconds.")