import json, regex, re, cloudscraper, time, sys
from bs4 import BeautifulSoup
import pandas as pd
from rich import print

cat_or_seller = 2 #1 Kategori 2 Satıcı
url = "https://www.trendyol.com/sr?mid=147054"
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

def makeHyperlink(url):
    return f'=Hyperlink("{url}","Ürün")'

def createExcelProductDetails(productLinks,urun_adedi):
    counter = 1
    df = pd.DataFrame(columns=['Ürün ID','Barkod','Ürün Adı','Ürün Özellikleri','Varyant','Fiyat','Fotoğraflar','Ürün Bilgileri','Teslimat Bilgisi', 'Link'])
    for link in productLinks:
        productDetailData = getGetProductDetailInfo(link) # Ürün linklerindeki ürünlerin detaylarını getir.
        if productDetailData == "Not Found":
            continue   
        product_name = productDetailData["product"]["name"]
        attr = productDetailData["product"]["attributes"]
        result = ""
        for at in attr:
            result = result + at['key']['name'] + " : " + at['value']['name'] + " | "
        product_attributes = result[:-2]
        product_variants = productDetailData['product']['variants']
        images = ['https://cdn.dsmcdn.com/' + img for img in productDetailData['product']['images']]
        img = ""
        for image in images:
            img = img + image +  " | "
        product_images = img[:-2]
        product_details = productDetailData["product"]["contentDescriptions"][0]["description"]
        product_delivery = productDetailData["product"]["deliveryInformation"]["deliveryDate"]
        product_link = 'https://www.trendyol.com'+productDetailData["product"]["url"]
        for variant in product_variants:
            attr = variant['attributeName']+":"+variant['attributeValue']
            urun_id = productDetailData["product"]["id"]
            barcode = variant['barcode']
            price = variant['price']['discountedPrice']['value']
            satir = {'Ürün ID':urun_id, 'Barkod': barcode, 'Ürün Adı':product_name, 'Ürün Özellikleri':product_attributes,'Varyant':attr,'Fiyat':price, 'Fotoğraflar':product_images,'Ürün Bilgileri':product_details,'Teslimat Bilgisi':product_delivery,'Link':product_link}
            print(counter," - ", product_name," - ", attr," - ", price," TL")
            df = df.append(satir, ignore_index=True)
        counter = counter + 1
        urun_adedi = urun_adedi - 1
        if urun_adedi == 0:
            break
    #print(df)
    df['Link'] = df.apply(lambda row : makeHyperlink(row['Link']), axis = 1)
    df.to_excel("output.xlsx") 

t0 = time.time()
print("Uygulama başladı.")
print("Linkler Toplanıyor...")
productPageUrls = createProductPageUrls(url,urun_adedi) # Ürün sayısına göre getirelecek sayfa linklerini oluştur (ürün sayısı / 24)
productLinks = getProductLinks(productPageUrls) # Sayfalarındaki ürün linklerini getir.
print(productLinks)
print("Ürün detayları çekiliyor...")
createExcelProductDetails(productLinks,urun_adedi) # Ürün detaylarıyla excel oluşturur.
t1 = time.time()
print(f"{t1-t0} saniye sürdü.")


def check_quit(inp):
    if inp == 'q':
        sys.exit(0)
x = str(input("Lütfen çıkmak için 'q' tuşuna basın: "))
check_quit(x)