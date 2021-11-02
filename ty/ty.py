from GetProducts import *
from GetProductInfo import *
import sqlite3,timeit
import pandas as pd
from rich import print

database = 'veritabani.sqlite'
url = "https://www.trendyol.com/kadin-sutyen-x-g1-c63"

def getProducts(url):
    products = GetProducts(url)
    productCount = products.getTotalProductCount()
    productPage = (productCount / 24) + 1
    urls = []
    for i in range(1,int(productPage)+1):
        urls.append(url+"?pi="+str(i))
    for url in urls:
        products = GetProducts(url)
        idAndUrl = products.getAllProductIdUrlToDB()

def getProductInfos():
    db = sqlite3.connect(database)
    cursor = db.cursor()
    #cursor.execute("CREATE TABLE IF NOT EXISTS product_details (product_id, product_name, product_brand, product_orginal_price,product_selling_price,product_discounted_price,product_rating_count,product_rating_average,product_comment_count,product_favorite_count,seller_name,seller_score,seller_tax_number,seller_city,seller_official_name,seller_count,product_all_sellers,product_url)")
    cursor.execute("select * from products")
    rows = cursor.fetchall()
    df = pd.DataFrame(columns=['Ürün ID','Barkod','Ürün Adı','Ürün Özellikleri','Varyant','Fiyat','Fotoğraflar','Ürün Bilgileri','Teslimat Bilgisi', 'Ürün Linki'])
    i = 0
    for row in rows:
        print(row[1])
        product = GetProductInfo(row[1])
        if product.control() == "Not Found"
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
            item_number = variant['itemNumber']
            barcode = variant['barcode']
            price = variant['price']['discountedPrice']['value']
            satir = {'Ürün ID':item_number, 'Barkod': barcode, 'Ürün Adı':product_name, 'Ürün Özellikleri':product_attributes,'Varyant':attr,'Fiyat':price, 'Fotoğraflar':product_images,'Ürün Bilgileri':product_details,'Teslimat Bilgisi':product_delivery,'Ürün Linki':product_link}
            #print(satir)
            df = df.append(satir, ignore_index=True)
        i=i+1
        if i == 100:
            break
    db.close()
    print(df)
    df.to_excel("output.xlsx") 


#getProducts(url)
getProductInfos()

