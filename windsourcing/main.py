import time,sqlite3,concurrent.futures,cloudscraper
from bs4 import BeautifulSoup
from rich import print

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
#insertAllLinks('sitemap-1.xml','SiteMapLinks')
#insertAllLinks('sitemap-2.xml','SiteMapLinks')
url = "https://www.windsourcing.com/en/3m-w9910-wind-tape-adhesion-promoter-473-ml-pint"
scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
data = scraper.get(url)
soup = BeautifulSoup(data.text, "html.parser")
product_title = soup.find("h1", class_="product--title").text.strip()
product_info = soup.find("ul", class_="product--base-info list--unstyled")
product_code = product_info.find("span").text.strip()

breadcrumb_list = soup.find("ul", class_="breadcrumb--list")
categories = []
for li in breadcrumb_list.find_all("li", {"role": "menuitem"}):
    categories.append(li.get_text(strip=True))
category = " > ".join(categories)
image_span = soup.find("span", class_="image--element")
data_img_original = image_span["data-img-original"]


print("URL: " + url)
print("Ürün Adı: " + product_title)
print("Ürün Kodu: " + product_code)
print("Ürün Kategorisi: " + category)
print("Ürün Fotoğraf Link: " + data_img_original)


t1 = time.time()
print(f"{t1-t0} seconds.")