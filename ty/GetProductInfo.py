import requests, json, regex, os
from lxml import html
from bs4 import BeautifulSoup
from rich import print

class GetProductInfo:

    global data
    
    def __init__(self,link):
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        #404 sayfaları engelle h1
        nf = soup.find("h1")
        if nf == "404":
            self.data = "Not Found"
        else:
            products = soup.find_all("script")[14]
            print(products)
            pattern = '\{(?:[^{}]|(?R))*\}'
            result = regex.search(pattern, str(products))
            if result is None:
                products = soup.find_all("script")[15]
                result = regex.search(pattern, str(products))[0]
            else:
                products = soup.find_all("script")[14]
                result = regex.search(pattern, str(products))[0]

            print(result)
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