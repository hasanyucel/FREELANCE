import json, regex, re, cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from rich import print

cat_or_seller = 1 #1 Kategori 2 Satıcı
url = "https://www.trendyol.com/cocuk-babet-x-g3-c113"
urun_adedi = 100


def getCategoryOrSellerProductsData(url):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
    data = scraper.get(url).content
    soup = BeautifulSoup(data, 'html.parser')
    products = soup.findAll('script', text = re.compile('__SEARCH_APP_INITIAL_STATE__'))
    pattern = '\{(?:[^{}]|(?R))*\}'
    result = regex.search(pattern, str(products[0]))[0]
    data = json.loads(result)
    return data

def createProductPageUrls(url,wantedProductCount):
    data = getCategoryOrSellerProductsData(url)
    totalProductCount = data["totalCount"] #Linkte bulunan toplam ürün adedi
    productPage = int((totalProductCount / 24) + 1) #Maksimum sayfa
    loopCount = int((wantedProductCount / 24) + 1) #Ürün Adedi İçin kaç sayfaya bakılacağı 
    urls = []
    for i in range(1,productPage+1):
            if cat_or_seller == 1:
                urls.append(url+"?pi="+str(i))
            elif cat_or_seller == 2:
                urls.append(url+"&pi="+str(i))
            else:
                break
            loopCount = loopCount - 1
            if loopCount == 0:
                break
    return urls

def getProductLinks(urls):
    products = []
    for url in urls:
        data = getCategoryOrSellerProductsData(url)
        for i in range (len(data["products"])):
            products.append('https://www.trendyol.com'+ data["products"][i]["url"])
    return products

def getGetProductDetailInfo(url):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
    data = scraper.get(url).content
    soup = BeautifulSoup(data, 'html.parser')
    nf = soup.find("h1").text
    if nf == "404":
        data = "Not Found"
    else:
        products = soup.findAll('script', text = re.compile('__PRODUCT_DETAIL_APP_INITIAL_STATE__'))
        pattern = '\{(?:[^{}]|(?R))*\}'
        result = regex.search(pattern, str(products[0]))[0]
        data = json.loads(result)
    return data

def createExcelProductDetails(productLinks,urun_adedi):
    for link in productLinks:
        productDetailData = getGetProductDetailInfo(link) # Ürün linklerindeki ürünlerin detaylarını getir.
        if productDetailData == "Not Found":
            continue

productPageUrls = createProductPageUrls(url,urun_adedi) # Ürün sayısına göre getirelecek sayfa linklerini oluştur (ürün sayısı / 24)
productLinks = getProductLinks(productPageUrls) # Sayfalarındaki ürün linklerini getir.
#print(productLinks)
createExcelProductDetails(productLinks,urun_adedi) # Ürün detaylarıyla excel oluşturur.
#print(productDetailData)