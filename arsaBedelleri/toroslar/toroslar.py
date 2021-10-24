from bs4 import BeautifulSoup
import requests,json,sqlite3,concurrent.futures,pandas as pd
from rich import print

db = "toroslarBelediyesi.sqlite"
r = requests.get("https://tahsilat.toroslar-bld.gov.tr/Emlak/RayicBedel")
MAX_THREADS = 30

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'birimFiyat' ('MahalleId' TEXT NOT NULL,'MahalleAdi' TEXT NOT NULL,'CaddeId' TEXT NOT NULL,'CaddeAdi' TEXT NOT NULL,'Yil' TEXT NOT NULL,'BirimFiyat' TEXT,PRIMARY KEY('MahalleId','CaddeId','Yil'));")
    conn.commit()
    conn.close()

def getYillar():
    soup = BeautifulSoup(r.content, 'html.parser')
    yillar_html = soup.find("select",attrs={'id':'YilID'})
    yillar_select = yillar_html.find_all("option")
    yillar = []
    for yil in yillar_select:
        if yil.text != "Yılı Seçiniz":
            yillar.append(yil.text)
    return yillar

def getMahalleler():
    soup = BeautifulSoup(r.content, 'html.parser')
    mahalleler_html = soup.find("select",attrs={'id':'TasinmazMahalleID'})
    mahalleler_select = mahalleler_html.find_all("option") 
    mahalleler = []
    for mahalle in mahalleler_select:
        if mahalle.text != 'Mahalleyi seçiniz':
            mahalleler.append(mahalle['value'])
            #print(mahalle['value'],mahalle.text)
    return mahalleler

def getCaddeSokaklar(mahalleKodu):
    url = f"https://tahsilat.toroslar-bld.gov.tr/Emlak/GetCaddeSokak?TasinmazMahalleID={mahalleKodu}"
    headers = {
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': 'ASP.NET_SessionId=r1l2jq4yska2nf21q1xjhcs1'
    }
    response = requests.request("GET", url, headers=headers)
    CaddeSokaklar = json.loads(response.text)
    caddeler = []
    for cadde in CaddeSokaklar:
        if cadde["TasinmazCaddeSokakID"] != 0:
            caddeler.append(cadde["TasinmazCaddeSokakID"])
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
    url = "https://tahsilat.toroslar-bld.gov.tr/Emlak/RayicBedel"
    payload = f'TasinmazCaddeSokakID={caddeKodu}&TasinmazMahalleID={mahalleKodu}&YilID={yil}'
    headers = {
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Cookie': 'ASP.NET_SessionId=r1l2jq4yska2nf21q1xjhcs1'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

def insertArsaBedeli(line):
    line2 = line.split(',')
    mahalleKodu = line2[1]
    caddeKodu = line2[2] 
    result = getArsaBedeli(line)
    soup = BeautifulSoup(result,'lxml')
    secililer = soup.find_all('option', selected=True)
    yil = secililer[1].text
    mah = secililer[2].text
    cadde = secililer[3].text
    deger = soup.select("#mytable > tbody > tr > td:nth-child(5)")
    if len(deger) != 0:
        print(deger)
        deger = deger[0].text.strip()
        deger = deger.split(' ')
        deger = deger[0]
    else:
        deger = '-'
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
    writer = pd.ExcelWriter('toroslar.xlsx')
    df1.to_excel(writer,sheet_name ='Toroslar')  
    writer.save()
    conn.close()

createDbAndTables()
#writeYilMahalleCaddeSokakToTXT()
#insertArsaBedeli("2021,181,13778")
"""lines = []
with open("mahCadSok.txt") as file:
    for line in file:
        line = line.replace("\n", "")
        lines.append(line)
        #insertArsaBedeli(line)
PoolExecutor(lines)"""
getPivotPrice()