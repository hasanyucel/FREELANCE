from bs4 import BeautifulSoup
import requests,json,sqlite3,concurrent.futures,pandas as pd
from rich import print

db = "mezitliBelediyesi.sqlite"
r = requests.get("https://e-belediye.mezitli.bel.tr/tr-tr/emlak/arsa-birim-degerleri")
MAX_THREADS = 30

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'birimFiyat' ('MahalleId' TEXT NOT NULL,'MahalleAdi' TEXT NOT NULL,'CaddeId' TEXT NOT NULL,'CaddeAdi' TEXT NOT NULL,'Yil' TEXT NOT NULL,'BirimFiyat' TEXT,PRIMARY KEY('MahalleId','CaddeId','Yil'));")
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
    soup = BeautifulSoup(r.content, 'html.parser')
    mahalleler_html = soup.find("select",attrs={'id':'MahalleId'})
    mahalleler_select = mahalleler_html.find_all("option") 
    mahalleler = []
    for mahalle in mahalleler_select:
        if mahalle['value'] != '0':
            mahalleler.append(mahalle['value'])
            print(mahalle['value'],mahalle.text)
    return mahalleler

def getCaddeSokaklar(mahalleKodu):
    url = f"https://e-belediye.mezitli.bel.tr/tr-tr/cadde-sokak?mahalleKodu={mahalleKodu}"
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
            #cur.execute("INSERT OR REPLACE INTO Caddeler (CaddeId,Cadde) VALUES (?,?)",(cadde["CaddeSokakKodu"],cadde["CaddeSokakAdi"]))
    return caddeler

def writeYilMahalleCaddeSokakToTXT():
    yillar = getYillar()
    mahalleler = getMahalleler()
    for mahalle in mahalleler:
        caddeler = getCaddeSokaklar(mahalle)
        for cadde in caddeler:
            for yil in yillar:
                print(yil,mahalle,cadde)
                with open("mahCadSok.txt", "a") as myfile:
                    myfile.write(str(yil)+','+str(mahalle)+','+str(cadde)+"\n")

def getArsaBedeli(line):
    line = line.split(',')
    yil = line[0]
    mahalleKodu = line[1]
    caddeKodu = line[2]
    url = "https://e-belediye.mezitli.bel.tr/tr-tr/emlak/arsa-birim-degerleri"
    payload=f'caddeKodu={caddeKodu}&mahalleKodu={mahalleKodu}&yil={yil}'
    headers = {
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': 'ASP.NET_SessionId=vixgacpnaan3mzxdg5jzbqyj; Culture=tr-tr'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

def insertArsaBedeli(line):
    line2 = line.split(',')
    mahalleKodu = line2[1]
    caddeKodu = line2[2]
    result = json.loads(getArsaBedeli(line))
    if (result["SonucAciklamasi"]=="Başarılı"):
        yil = result["ArsaBirimFiyatListesi"][0]["Yil"]
        mah = result["ArsaBirimFiyatListesi"][0]["MahalleAdi"]
        cadde = result["ArsaBirimFiyatListesi"][0]["CaddeSokakAdi"]
        deger = result["ArsaBirimFiyatListesi"][0]["ArsaBirimDegeri"]
        print(mahalleKodu,mah,caddeKodu,cadde,yil,deger)
        insertMahCadPrice(mahalleKodu,mah,caddeKodu,cadde,yil,deger)
        
def insertMahCadPrice(MahalleId,MahalleAdi,CaddeId,CaddeAdi,Yil,BirimFiyat):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO birimFiyat (MahalleId,MahalleAdi,CaddeId,CaddeAdi,Yil,BirimFiyat) VALUES (?,?,?,?,?,?)",(MahalleId,MahalleAdi,CaddeId,CaddeAdi,Yil,BirimFiyat))
    conn.commit()
    conn.close()

def PoolExecutor(line):  
    threads = min(MAX_THREADS, len(line))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(insertArsaBedeli, line)

def getPivotPrice():
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("select t.MahalleAdi,t.CaddeAdi,t.Yil,t.BirimFiyat from birimFiyat t order by t.MahalleAdi,t.CaddeAdi,t.Yil", conn)
    df = pd.DataFrame(df)
    df1 = df.pivot_table(index =['MahalleAdi','CaddeAdi'], columns ='Yil', values ='BirimFiyat',aggfunc='first')
    writer = pd.ExcelWriter('mezitli.xlsx')
    df1.to_excel(writer,sheet_name ='Mezitli')  
    writer.save()
    conn.close()


createDbAndTables()
#writeYilMahalleCaddeSokakToTXT()

lines = []
with open("mahCadSok.txt") as file:
    for line in file:
        line = line.replace("\n", "")
        lines.append(line)
        #insertArsaBedeli(line)
PoolExecutor(lines)
getPivotPrice()