import requests, json, regex, os, re, cloudscraper
from lxml import html
from bs4 import BeautifulSoup
from rich import print

class GetProductInfo:

    global data
    
    def __init__(self,link):
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
        data = scraper.get(link).content
        soup = BeautifulSoup(data, 'html.parser')
        nf = soup.find("h1").text
        if nf == "404":
            self.data = "Not Found"
        else:
            products = soup.findAll('script', text = re.compile('__PRODUCT_DETAIL_APP_INITIAL_STATE__'))
            pattern = '\{(?:[^{}]|(?R))*\}'
            result = regex.search(pattern, str(products[0]))[0]
            self.data = json.loads(result)

    def control(self):
        return self.data    
    
    def getProductID(self):
        return self.data["product"]["id"]

    def getProductName(self):
        return self.data["product"]["name"]

    def getProductURL(self):
        return 'https://www.trendyol.com'+self.data["product"]["url"]

    def getAllProductData(self):
        return self.data["product"]

    def getAttributes(self):
        attr = self.data["product"]["attributes"]
        result = ""
        for at in attr:
            result = result + at['key']['name'] + " : " + at['value']['name'] + " | "
        return result[:-2]

    def getImages(self):
        images = ['https://cdn.dsmcdn.com/' + img for img in self.data['product']['images']]
        result = ""
        for image in images:
            result = result + image +  " | "
        return result[:-2]
    
    def getDeliveryInformation(self):
        return self.data["product"]["deliveryInformation"]["deliveryDate"]
    
    def getDetails(self):
        return self.data["product"]["contentDescriptions"][0]["description"]