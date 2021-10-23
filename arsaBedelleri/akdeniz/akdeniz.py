from bs4 import BeautifulSoup
import requests,json,sqlite3
from rich import print

r = requests.get("https://e-belediye.akdeniz.bel.tr/tr-tr/emlak/arsa-birim-degerleri")

db = "akdeniz.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Mahalleler' ('MahalleId' TEXT NOT NULL,'Mahalle' TEXT NOT NULL,PRIMARY KEY('MahalleId'));")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Caddeler' ('CaddeId' TEXT NOT NULL,'Cadde' TEXT NOT NULL,PRIMARY KEY('CaddeId'));")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS 'Fiyat' ('MahalleId' TEXT NOT NULL,'CaddeId' TEXT NOT NULL,'Yil' TEXT NOT NULL,'BirimFiyat' TEXT,PRIMARY KEY('MahalleId','CaddeId','Yil'));")
    conn.commit()
    conn.close()

def getYillar():
    soup = BeautifulSoup(r.content, 'html.parser')
    yillar_html = soup.find("select",attrs={'id':'yil'})
    yillar_select = yillar_html.find_all("option")
    yillar = []
    for yil in yillar_select:
        yillar.append(yil.text)
    return yillar

def getMahalleler():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    soup = BeautifulSoup(r.content, 'html.parser')
    mahalleler_html = soup.find("select",attrs={'id':'MahalleId'})
    mahalleler_select = mahalleler_html.find_all("option") #ilk iki value gereksiz
    mahalleler = []
    for mahalle in mahalleler_select:
        mahalleler.append(mahalle['value'])
        cur.execute("INSERT OR REPLACE INTO Mahalleler (MahalleId,Mahalle) VALUES (?,?)",(mahalle['value'],mahalle.text))
        conn.commit()
    conn.close()
        #print(mahalle['value'],mahalle.text) DB insert et
    return mahalleler

def getCaddeSokaklar(mahalleKodu):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    url = f"https://e-belediye.akdeniz.bel.tr/tr-tr/cadde-sokak?mahalleKodu={mahalleKodu}"
    headers = {
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': 'ASP.NET_SessionId=vixgacpnaan3mzxdg5jzbqyj; Culture=tr-tr'
    }
    response = requests.request("GET", url, headers=headers)
    result = json.loads(response.text)
    SonucAciklamasi = result["SonucAciklamasi"]
    print(SonucAciklamasi)
    CaddeSokaklar = result["CaddeSokaklar"]
    caddeler = []
    for cadde in CaddeSokaklar:
        if cadde["CaddeSokakKodu"] != 0:
            caddeler.append(cadde["CaddeSokakKodu"])
            cur.execute("INSERT OR REPLACE INTO Caddeler (CaddeId,Cadde) VALUES (?,?)",(cadde["CaddeSokakKodu"],cadde["CaddeSokakAdi"]))
            conn.commit()
    conn.close()
    return caddeler

createDbAndTables()
yillar = getYillar()
mahalleler = getMahalleler()
conn = sqlite3.connect(db)
cur = conn.cursor()
for mahalle in mahalleler:
    caddeler = getCaddeSokaklar(mahalle)
    for cadde in caddeler:
        for yil in yillar:
            cur.execute("INSERT OR REPLACE INTO Fiyat (MahalleId,CaddeId,Yil) VALUES (?,?,?)",(mahalle,cadde,yil))
            conn.commit()
            print(yil,mahalle,cadde)
conn.close()
