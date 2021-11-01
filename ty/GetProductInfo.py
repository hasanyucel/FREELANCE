import requests, json, regex, os
from lxml import html
from bs4 import BeautifulSoup

class GetProductInfo:

    global data
    
    #import json
    #import requests
    #from bs4 import BeautifulSoup
    #
    #url = "https://www.trendyol.com/xiaomi/64mp-note-9-pro-6gb-64gb-6-67-yesil-akilli-cep-telefonu-p-58882069"
    #r = requests.get(url)
    #soup = BeautifulSoup(r.content,'html.parser')
    #script = soup.findAll('script')[11]
    #fi = str(script).find('{')
    #li = str(script).rfind('}') + 1
    #data = str(script)[fi:li]
    #
    #print(json.loads(data))

    def __init__(self,link):
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.find_all("script")[14]
        pattern = '\{(?:[^{}]|(?R))*\}'
        result = regex.search(pattern, str(products)).group(0)
        self.data = json.loads(result)
        
    def getProductID(self):
        return self.data["product"]["id"]

    def saveImages(self):
        images = ['https://cdn.dsmcdn.com/' + img for img in self.data['product']['images']]
        if not os.path.exists('images/'+str(self.data["product"]["id"])+''):
            os.makedirs('images/'+str(self.data["product"]["id"])+'')
        i = 1
        for image in images:
            response = requests.get(image)
            file = open('images/'+str(self.data["product"]["id"])+'/'+str(i)+'.jpg', 'wb')
            file.write(response.content)
            file.close()
            i = i + 1

    def getProductName(self):#
        return self.data["product"]["name"]

    def getProductOrginalPrice(self):
        return self.data["product"]["price"]["originalPrice"]["value"]

    def getProductSellingPrice(self):
        return self.data["product"]["price"]["sellingPrice"]["value"]
    
    def getProductDiscountedPrice(self):
        return self.data["product"]["price"]["discountedPrice"]["value"]

    def getProductBrand(self):
        return self.data["product"]["metaBrand"]["name"]

    def getProductSellerName(self):
        return self.data["product"]["merchant"]["name"]
    
    def getProductSellerScore(self):
        try:
            return self.data["product"]["merchant"]["sellerScore"]
        except:
            return "-"

    def getProductSellerCityName(self):
        return self.data["product"]["merchant"]["cityName"]

    def getProductSellerOfficialName(self):
        return self.data["product"]["merchant"]["officialName"]
    
    def getProductSellerTaxNumber(self):
        return self.data["product"]["merchant"]["taxNumber"]

    def getProductURL(self):
        return 'https://www.trendyol.com'+self.data["product"]["url"]

    def getProductRatingCount(self):
        return self.data["product"]["ratingScore"]["totalRatingCount"]

    def getProductAverageRating(self):
        return self.data["product"]["ratingScore"]["averageRating"]

    def getProductTotalCommentCount(self):
        return self.data["product"]["ratingScore"]["totalCommentCount"]

    def getProductFavoriteCount(self):
        return self.data["product"]["favoriteCount"]

    def getAllProductData(self):
        return self.data["product"]

    def getProductMerhactCount(self):
        return len(self.data["product"]["otherMerchants"]) + 1

    def getProductAllMerchantNames(self):
        merchants = ""
        count = len(self.data["product"]["otherMerchants"])
        for i in range (count):
            merchants = merchants + "," + self.data["product"]["otherMerchants"][i]["merchant"]["name"]
        return self.data["product"]["merchant"]["name"]+merchants
    
    def getProductBarcode(self):
        return self.data["product"]["variants"][0]["barcode"]

    def getAttributes(self):#
        attr = self.data["product"]["attributes"]
        result = ""
        for at in attr:
            result = result + at['key']['name'] + " : " + at['value']['name'] + " | "
        return result[:-2]

    def getImages(self):#
        images = ['https://cdn.dsmcdn.com/' + img for img in self.data['product']['images']]
        result = ""
        for image in images:
            result = result + image +  " | "
        return result[:-2]
    
    def getDeliveryInformation(self):#
        return self.data["product"]["deliveryInformation"]["deliveryDate"]
    
    def getDetails(self):
        return self.data["product"]["contentDescriptions"][0]["description"]