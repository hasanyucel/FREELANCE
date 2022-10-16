import requests,time,sqlite3
from bs4 import BeautifulSoup
from rich import print
db = "tumpaelektrik.sqlite"
def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'ProductDetails' ('Url' TEXT, 'Reference' TEXT, 'Name' TEXT, 'Price' REAL, 'Stock' TEXT, PRIMARY KEY('Reference'));")
    cur.execute("CREATE TABLE IF NOT EXISTS 'ProductLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    conn.commit()

def insertAllLinks(page,table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    payload={}
    headers = {
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'host': 'online.tumpaelektrik.com'
    }
    response = requests.get(page, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'lxml')
    productUrlList = soup.find('div',attrs={'class':'product-listing row'})
    productUrlList = soup.find_all('div',attrs={'class':'product__inside__image'})
    for productUrl in productUrlList:
        url = "https://online.tumpaelektrik.com" + productUrl.a["href"]
        cur.execute(f"INSERT OR IGNORE INTO {table_name} (URL) VALUES (?)",(url,))
    conn.commit()
    conn.close()

def getProductLinks():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT Url FROM ProductLinks')
    links = cur.fetchall()
    links = [f[0] for f in links]
    conn.close()
    return links

def getProductDetail(counter,productUrl,table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    payload={}
    headers = {
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'host': 'online.tumpaelektrik.com'
    }
    response = requests.get(productUrl, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'lxml')
    productRefStock = soup.find('div',attrs={'class':'wrapper hidden-xs'})
    productReference = productRefStock.select('strong')[0].text
    productStock = productRefStock.select('strong')[1].text
    productPrice = soup.find('div',attrs={'class':'price-box product-info__price'}).span.text
    productPrice = productPrice.replace('₺ + KDV','')
    productName = soup.find('div',attrs={'class':'product-info__title'}).h1.text
    print(str(counter) + ') ' + productUrl + ' --- ' + productReference + ' --- ' + productName + ' --- ' + productStock + ' --- ' + productPrice)
    cur.execute(f"INSERT OR IGNORE INTO {table_name} (Url,Reference,Name,Price,Stock) VALUES (?,?,?,?,?)",(productUrl,productReference,productName,productPrice,productStock))
    conn.commit()
    conn.close()

print("Script is working...")
t0 = time.time()
createDbAndTables()
#x = range(1, 8)
#for n in x:
#    pageNum = f'https://online.tumpaelektrik.com/Kategori/aydinlatma?PageSize=96&Page={n}' #Tüm ürünlerin linkini toplar
#    insertAllLinks(pageNum,'ProductLinks')
linkList = getProductLinks() #Toplanan ürün linklerini getirir.
counter = 0
for link in linkList:
    counter = counter + 1
    getProductDetail(counter, link, 'ProductDetails') #Ürüne ait referans, ad, stok ve fiyat bilgisini çeker

t1 = time.time()
print(f"{t1-t0} seconds.")