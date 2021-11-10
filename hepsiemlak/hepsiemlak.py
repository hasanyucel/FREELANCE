import cloudscraper, json, time, unidecode
from dateutil import parser
from rich import print
from random import randint

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
    print(BanyoSayisi)
    
#createApiUrls()
#api_urls = readUrlsFromTXT("apis.txt")
data = getAllSaleDetailData("https://www.hepsiemlak.com/api/realties/111267-748")
parseJsonDetails(data)