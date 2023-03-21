import time,sqlite3,concurrent.futures
from bs4 import BeautifulSoup

db = "windsourcing.sqlite"


def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    conn.commit()

def insertAllLinks(xml,table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    counter = 1
    with open(xml) as f:
        xml_dosyasi = f.read()
        soup = BeautifulSoup(xml_dosyasi, 'xml')

        urls = [loc.string for loc in soup.find_all('loc')]
        for url in urls:
            print(str(counter) + " - " + url)
            counter +=1
            cur.execute(f"INSERT OR IGNORE INTO {table_name} (URL) VALUES (?)",(url,))
            conn.commit()
    conn.close()

def getSitemapLinks(table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f'SELECT Url FROM {table_name}')
    links = cur.fetchall()
    links = [f[0] for f in links]
    conn.close()
    return links

print("Script is working...")
t0 = time.time()
createDbAndTables()
insertAllLinks('sitemap-2.xml','SiteMapLinks')


t1 = time.time()
print(f"{t1-t0} seconds.")