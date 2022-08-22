import requests,json,sqlite3
from rich import print

db = "camkirangaraj.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Urunler' ('UrunId' TEXT NOT NULL,'Link' TEXT NOT NULL,'UrunAdi' TEXT NOT NULL,'UrunKodu' TEXT NOT NULL,'Fiyat' NUMERIC NOT NULL,PRIMARY KEY('UrunId'));")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Detaylar' ('UrunId' TEXT NOT NULL,'UrunKategorisi' TEXT NOT NULL,'UrunAciklama' TEXT NOT NULL,'Resim1' TEXT NOT NULL,'Resim2' TEXT NOT NULL,'Resim3' TEXT NOT NULL,'Resim4' TEXT NOT NULL,'Resim5' TEXT NOT NULL,'Resim6' TEXT NOT NULL,PRIMARY KEY('UrunId'));")
    conn.commit()
    conn.close()

def getAllProductData(pcount):
    url = f"https://camkirangaraj.com/products/?from=0&json=true&to={pcount}"
    scraper = requests.get(url)
    data = scraper.content
    result = json.loads(data)
    return result

createDbAndTables()
productData = getAllProductData(10)
print(productData)