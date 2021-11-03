from GetProducts import *
from GetProductInfo import *
import sqlite3,timeit
import pandas as pd
from rich import print

database = 'veritabani.sqlite'
url = "https://www.trendyol.com/sr?mid=147054"
urun_adedi = 10

def getProductsUrl(url):
    products = GetProducts(url)
    productCount = products.getTotalProductCount()
    productPage = int((productCount / 24) + 1)
    loop_count = int((urun_adedi / 24) + 1)
    urls = []
    for i in range(1,productPage+1):
        urls.append(url+"?pi="+str(i))
        loop_count = loop_count - 1
        if loop_count == 0:
            break
    for url in urls:
        products = GetProducts(url)
        idAndUrl = products.getAllProductIdUrlToDB()

def getProductInfos():
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute("select * from products")
    rows = cursor.fetchall()
    df = pd.DataFrame(columns=['Ürün ID','Barkod','Ürün Adı','Ürün Özellikleri','Varyant','Fiyat','Fotoğraflar','Ürün Bilgileri','Teslimat Bilgisi', 'Ürün Linki'])
    loop_count = urun_adedi
    for row in rows:
        print(row[1])
        product = GetProductInfo(row[1])
        if product.control() == "Not Found":
            continue
        product_all_data = product.getAllProductData()
        product_name = product.getProductName()
        product_attributes = product.getAttributes()
        product_variants = product_all_data['variants']
        product_images = product.getImages()
        product_details = product.getDetails()
        product_delivery = product.getDeliveryInformation()
        product_link = product.getProductURL()
        print(product_attributes)
        for variant in product_variants:
            attr = variant['attributeName']+":"+variant['attributeValue']
            urun_id = product.getProductID()
            barcode = variant['barcode']
            price = variant['price']['discountedPrice']['value']
            satir = {'Ürün ID':urun_id, 'Barkod': barcode, 'Ürün Adı':product_name, 'Ürün Özellikleri':product_attributes,'Varyant':attr,'Fiyat':price, 'Fotoğraflar':product_images,'Ürün Bilgileri':product_details,'Teslimat Bilgisi':product_delivery,'Ürün Linki':product_link}
            df = df.append(satir, ignore_index=True)
        loop_count = loop_count - 1
        if loop_count == 0:
            break
    cursor.execute("delete from products")
    db.commit()
    db.close()
    print(df)
    df.to_excel("output.xlsx") 


getProductsUrl(url)
getProductInfos()

