import cloudscraper, json, time, unidecode, sqlite3, pandas as pd
from bs4 import BeautifulSoup
from dateutil import parser
from rich import print
from random import randint

db = "hepsiemlak.sqlite"

def getAllSaleData(page):
    url = f"https://www.hepsiemlak.com/api/realty-list/ankara-satilik?page={page}&fillIntentUrls=false"
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
    data = scraper.get(url).content
    result = json.loads(data)
    return result["realtyList"]

def createApiUrls():
    for i in range (1,1119,1):
        sales = getAllSaleData(i)
        time.sleep(randint(1,4))
        for sale in sales:
            proje = sale["projeland"]
            listingId = sale["listingId"]
            if proje:
                api = f"https://www.hepsiemlak.com/api/proje/projeland_{listingId}" #continue
            else:
                api = f"https://www.hepsiemlak.com/api/realties/{listingId}"
            with open("apis.txt", "a") as myfile:
                myfile.write(api+"\n")

def readUrlsFromTXT(path): #TXT dosyalarındaki satırları liste olarak döner.
    urls = []
    f = open(path,'r') #'__location__+\kelime\A.txt'
    for line in f:
        line = unidecode.unidecode(line.strip())
        line = line.replace(' ','').lower()
        urls.append(line)
    return urls

def getAllSaleDetailData(api_url):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
    data = scraper.get(api_url).content
    if data == b'':
        return "-"
    else:
        result = json.loads(data)
        return result

def insertAttribute(atid,name,table):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"INSERT OR IGNORE INTO {table} (Id,Tanim) VALUES (?,?)",(atid,name))
    conn.commit()
    conn.close()

def insertSaleData(IlanBasligi,Il,Ilce,Mahalle,Lon,Lat,Fiyat,IlanNo,SonGuncellemeTarihi,\
        IlanDurumu,KonutSekli,OdaSayisi,BrutNetM2,BulunduguKat,BinaninYasi,IsinmaTipi,BinadaKatSayisi,\
            KrediyeUygun,EsyaDurumu,BanyoSayisi,YapiTipi,YapininDurumu,KullanimDurumu,TapuDurumu,Aidat,Takas,\
                Cephe,SiteIcerisinde,KiraGetirisi,YakitTipi,YetkiliOfis,GoruntuluArama,at1,at2,at3,Link,IlanAciklamasi):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"INSERT OR REPLACE INTO sales (IlanBasligi,Il,Ilce,Mahalle,Lon,Lat,Fiyat,IlanNo,SonGuncellemeTarihi,\
        IlanDurumu,KonutSekli,OdaSayisi,BrutNetM2,BulunduguKat,BinaninYasi,IsinmaTipi,BinadaKatSayisi,\
            KrediyeUygun,EsyaDurumu,BanyoSayisi,YapiTipi,YapininDurumu,KullanimDurumu,TapuDurumu,Aidat,Takas,\
                Cephe,SiteIcerisinde,KiraGetirisi,YakitTipi,YetkiliOfis,GoruntuluArama,Attrs1,Attrs2,Attrs3,Url,Aciklama) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(IlanBasligi,Il,Ilce,Mahalle,Lon,Lat,Fiyat,IlanNo,SonGuncellemeTarihi,\
        IlanDurumu,KonutSekli,OdaSayisi,BrutNetM2,BulunduguKat,BinaninYasi,IsinmaTipi,BinadaKatSayisi,\
            KrediyeUygun,EsyaDurumu,BanyoSayisi,YapiTipi,YapininDurumu,KullanimDurumu,TapuDurumu,Aidat,Takas,\
                Cephe,SiteIcerisinde,KiraGetirisi,YakitTipi,YetkiliOfis,GoruntuluArama,at1,at2,at3,Link,IlanAciklamasi))
    conn.commit()
    conn.close()

def parseJsonDetails(data):
    if data != "-":
        IlanNo = data["realtyDetail"]["listingId"]
        IlanBasligi = data["realtyDetail"]["title"]
        Il = data["realtyDetail"]["city"]["name"]
        Ilce = data["realtyDetail"]["county"]["name"]
        Mahalle = data["realtyDetail"]["district"]["name"]
        Lat = data["realtyDetail"]["mapLocation"]["lat"]
        Lon = data["realtyDetail"]["mapLocation"]["lon"]
        Fiyat = str(data["realtyDetail"]["price"]) + " " + data["realtyDetail"]["currency"]
        SonGuncellemeTarihi = data["realtyDetail"]["listingUpdatedDate"]
        SonGuncellemeTarihi = SonGuncellemeTarihi.split('T')
        SonGuncellemeTarihi = SonGuncellemeTarihi[0]
        IlanDurumu = data["realtyDetail"]["category"]["typeName"]
        KonutSekli = data["realtyDetail"]["subCategory"]["typeName"]
        OdaSayisi = data["realtyDetail"]["roomAndLivingRoom"][0]
        BrutNetM2 = str(data["realtyDetail"]["sqm"]["grossSqm"][0]) + " m2 / " + str(data["realtyDetail"]["sqm"]["netSqm"]) + " m2"
        if data["realtyDetail"]["floor"] is not None:
            BulunduguKat = data["realtyDetail"]["floor"]["name"]
        else:
            BulunduguKat = "NULL" 
        if data["realtyDetail"]["age"] is not None:
            BinaninYasi = data["realtyDetail"]["age"]
        else:
            BinaninYasi = "NULL"
        if data["realtyDetail"]["heating"] is not None:
            IsinmaTipi = data["realtyDetail"]["heating"]["name"]
        else:
            IsinmaTipi = "NULL" 
        if data["realtyDetail"]["floor"] is not None:
            BinadaKatSayisi = data["realtyDetail"]["floor"]["count"]
        else:
            BinadaKatSayisi = "NULL"    
        if data["realtyDetail"]["credit"] is not None:
            KrediyeUygun = data["realtyDetail"]["credit"]["name"]
        else:
            KrediyeUygun = "NULL" 
        if data["realtyDetail"]["furnished"] is not None:
            EsyaDurumu = data["realtyDetail"]["furnished"]
        else:
            EsyaDurumu = "NULL" 
        if EsyaDurumu:
            EsyaDurumu = "Eşyalı"
        else:
            EsyaDurumu = "Eşyalı Değil"
        if data["realtyDetail"]["bathRoom"] is not None:
            BanyoSayisi = str(data["realtyDetail"]["bathRoom"])
        else:
            BanyoSayisi = "NULL" 
        if data["realtyDetail"]["build"] is not None:
            YapiTipi = data["realtyDetail"]["build"]["name"]
        else:
            YapiTipi = "NULL"
        if data["realtyDetail"]["buildState"] is not None:
            YapininDurumu = data["realtyDetail"]["buildState"]["name"]
        else:
            YapininDurumu = "NULL"
        if data["realtyDetail"]["usage"] is not None:
            KullanimDurumu = data["realtyDetail"]["usage"]["name"]
        else:
            KullanimDurumu = "NULL"
        if data["realtyDetail"]["landRegisterName"] is not None:
            TapuDurumu = data["realtyDetail"]["landRegisterName"]
        else:
            TapuDurumu = "NULL"
        if data["realtyDetail"]["fee"] is not None:
            if data["realtyDetail"]["fee"]["amount"] is not None:
                if data["realtyDetail"]["fee"]["currencyCode"] is not None:
                    Aidat = str(data["realtyDetail"]["fee"]["amount"]) + " " + data["realtyDetail"]["fee"]["currencyCode"]
                else:
                    Aidat = "NULL"
            else:
                Aidat = "NULL"
        else:
            Aidat = "NULL"
        if data["realtyDetail"]["barter"] is not None:
            Takas = data["realtyDetail"]["barter"]["name"]
        else:
            Takas = "NULL"
        if data["realtyDetail"]["sides"] is not None:
            Cephe = data["realtyDetail"]["sides"]
            Cephe = ", ".join(str(x["name"]) for x in Cephe)
        else:
            Cephe = "NULL"
        if data["realtyDetail"]["housingComplex"] is not None:
            SiteIcerisinde = data["realtyDetail"]["housingComplex"]["name"]
        else:
            SiteIcerisinde = "NULL"
        if data["realtyDetail"]["rental"] is not None:
            if data["realtyDetail"]["rental"]["currencyCode"] is not None:
                KiraGetirisi = str(data["realtyDetail"]["rental"]["amount"]) + " " + data["realtyDetail"]["rental"]["currencyCode"]
            else:
                KiraGetirisi = "NULL"
        else:
            KiraGetirisi = "NULL"
        if data["realtyDetail"]["fuel"] is not None:
            YakitTipi = data["realtyDetail"]["fuel"]["name"]
        else:
            YakitTipi = "NULL"
        if data["realtyDetail"]["authorizedRealtor"] is not None:
            YetkiliOfis = data["realtyDetail"]["authorizedRealtor"]
        else:
            YetkiliOfis = "NULL"
        if data["realtyDetail"]["onlineVisit"] is not None:
            GoruntuluArama = data["realtyDetail"]["onlineVisit"]
        else:
            GoruntuluArama = "NULL"  
        if data["realtyDetail"]["description"] is not None:
            IlanAciklamasiHTML = data["realtyDetail"]["description"]
            IlanAciklamasi = BeautifulSoup(IlanAciklamasiHTML, "lxml").text.strip()
        else:
            IlanAciklamasi = "NULL"
        Link = "https://www.hepsiemlak.com/"+data["realtyDetail"]["detailUrl"]
        if data["realtyDetail"]["attributes"] is not None:
            attrs1 = data["realtyDetail"]["attributes"]["inAttributes"]
            at1 = ",".join(str(x["id"]) for x in attrs1)
            for at in attrs1:
                insertAttribute(str(at["id"]),at["name"],"ozellik1")
            attrs2 = data["realtyDetail"]["attributes"]["outAttributes"]
            at2 = ",".join(str(x["id"]) for x in attrs2)
            for at in attrs2:
                insertAttribute(str(at["id"]),at["name"],"ozellik2")
            attrs3 = data["realtyDetail"]["attributes"]["locationAttributes"]
            at3 = ",".join(str(x["id"]) for x in attrs3)
            for at in attrs3:
                insertAttribute(str(at["id"]),at["name"],"ozellik3")
        else:
            at1 = "NULL"
            at2 = "NULL"
            at3 = "NULL"
        insertSaleData(IlanBasligi,Il,Ilce,Mahalle,Lon,Lat,Fiyat,IlanNo,SonGuncellemeTarihi,\
            IlanDurumu,KonutSekli,OdaSayisi,BrutNetM2,BulunduguKat,BinaninYasi,IsinmaTipi,BinadaKatSayisi,\
                KrediyeUygun,EsyaDurumu,BanyoSayisi,YapiTipi,YapininDurumu,KullanimDurumu,TapuDurumu,Aidat,Takas,\
                    Cephe,SiteIcerisinde,KiraGetirisi,YakitTipi,YetkiliOfis,GoruntuluArama,at1,at2,at3,Link,IlanAciklamasi)

def insertIlanNos(table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f'select IlanNo from sales')
    links = cur.fetchall()
    for f in links:
        cur.execute(f"INSERT OR REPLACE INTO {table_name} (IlanNo) VALUES (?)",(f[0],))
    conn.commit()
    conn.close()

def fillAttrs(attr,table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f'select IlanNo,{attr} from sales')
    links = cur.fetchall()
    for f in links:
        if f[1] != "" and f[1] != "NULL":
            print(f)
            x = f[1].split(",")
            for at in x:
                cur.execute(f"UPDATE {table_name} set '{at}' = 'VAR' where IlanNo = '{f[0]}'")
            conn.commit()
    conn.close()

def makeHyperlink(url):
    return f'=Hyperlink("{url}","İlan")'

def makeLocationHyperlink(lat,lon):
    return f'=Hyperlink("http://www.google.com/maps/place/{lat},{lon}","Konum")'

def getPivotSales():
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("SELECT s.*,i.*,d.*,k.* from sales s, icOzellikler i, disOzellikler d, konum k WHERE s.IlanNo = i.IlanNo AND s.IlanNo = d.IlanNo AND s.IlanNo = k.IlanNo", conn)
    df = pd.DataFrame(df)
    df['Url'] = df.apply(lambda row : makeHyperlink(row['Url']), axis = 1)
    df['Konum'] = df.apply(lambda row : makeLocationHyperlink(row['Lat'],row['Lon']), axis = 1)
    print(df)
    writer = pd.ExcelWriter('hepsiEmlak.xlsx')
    df.to_excel(writer,sheet_name ='Emlak')
    writer.save()
    conn.close()
"""createApiUrls()
api_urls = readUrlsFromTXT("apis.txt")
for url in api_urls:
    time.sleep(randint(1,3))
    print(url)
    data = getAllSaleDetailData(url)
    parseJsonDetails(data)"""
#insertIlanNos("konum")
#fillAttrs("Attrs3","konum")
getPivotSales()