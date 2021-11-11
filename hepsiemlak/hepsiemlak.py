import cloudscraper, json, time, unidecode, sqlite3
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
                api = f"https://www.hepsiemlak.com/api/proje/projeland_{listingId}"
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
    BulunduguKat = data["realtyDetail"]["floor"]["name"]
    BinaninYasi = data["realtyDetail"]["age"]
    IsinmaTipi = data["realtyDetail"]["heating"]["name"]
    BinadaKatSayisi = data["realtyDetail"]["floor"]["count"]
    KrediyeUygun = data["realtyDetail"]["credit"]["name"]
    EsyaDurumu = data["realtyDetail"]["furnished"]
    if EsyaDurumu:
        EsyaDurumu = "Eşyalı"
    else:
        EsyaDurumu = "Eşyalı Değil"
    BanyoSayisi = str(data["realtyDetail"]["bathRoom"])
    YapiTipi = data["realtyDetail"]["build"]["name"]
    YapininDurumu = data["realtyDetail"]["buildState"]["name"]
    KullanimDurumu = data["realtyDetail"]["usage"]["name"]
    TapuDurumu = data["realtyDetail"]["landRegisterName"]
    if data["realtyDetail"]["fee"] is not None:
        Aidat = str(data["realtyDetail"]["fee"]["amount"]) + " " + data["realtyDetail"]["fee"]["currencyCode"]
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
    KiraGetirisi = str(data["realtyDetail"]["rental"]["amount"]) + " " + data["realtyDetail"]["rental"]["currencyCode"]
    YakitTipi = data["realtyDetail"]["fuel"]["name"]
    if data["realtyDetail"]["authorizedRealtor"] is not None:
        YetkiliOfis = data["realtyDetail"]["authorizedRealtor"]
    else:
        YetkiliOfis = "NULL"
    GoruntuluArama = data["realtyDetail"]["onlineVisit"]
    IlanAciklamasiHTML = data["realtyDetail"]["description"]
    IlanAciklamasi = BeautifulSoup(IlanAciklamasiHTML, "lxml").text.strip()
    Link = "https://www.hepsiemlak.com/"+data["realtyDetail"]["detailUrl"]
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
    insertSaleData(IlanBasligi,Il,Ilce,Mahalle,Lon,Lat,Fiyat,IlanNo,SonGuncellemeTarihi,\
        IlanDurumu,KonutSekli,OdaSayisi,BrutNetM2,BulunduguKat,BinaninYasi,IsinmaTipi,BinadaKatSayisi,\
            KrediyeUygun,EsyaDurumu,BanyoSayisi,YapiTipi,YapininDurumu,KullanimDurumu,TapuDurumu,Aidat,Takas,\
                Cephe,SiteIcerisinde,KiraGetirisi,YakitTipi,YetkiliOfis,GoruntuluArama,at1,at2,at3,Link,IlanAciklamasi)
    
#createApiUrls()
#api_urls = readUrlsFromTXT("apis.txt")
data = getAllSaleDetailData("https://www.hepsiemlak.com/api/realties/4180-8445")
parseJsonDetails(data)