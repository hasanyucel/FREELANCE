import cloudscraper, json, time
from rich import print
from random import randint

def getAllSaleData(page):
    url = f"https://www.hepsiemlak.com/api/realty-list/ankara-satilik?page={page}&fillIntentUrls=false"
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
    data = scraper.get(url).content
    result = json.loads(data)
    return result["realtyList"]

def createApiUrl():
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
        
createApiUrl()