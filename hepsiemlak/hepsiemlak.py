import cloudscraper, json, time, unidecode
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

#createApiUrls()
print(readUrlsFromTXT("apis.txt"))