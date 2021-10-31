from GetProducts import *
from GetProductInfo import *
import sqlite3,timeit
import pandas as pd
from rich import print

database = 'veritabani.sqlite'
url = "https://www.trendyol.com/soundbar-x-c143233"

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
    df = pd.DataFrame(columns=['Ürün ID','Ürün Adı','Marka','Orjinal Fiyat','Satış Fiyatı','İndirimli Fiyat','Değerlendirme Sayısı','Değerlendirme Ortalaması','Yorum Sayısı','Favori Sayısı','Satıcı Adı','Satıcı Puanı','Satıcı Vergi No','Satıcı Şehiri','Satıcı Şirket Adı','Ürünü Satan Sayısı','Tüm Satıcılar','Ürün Linki'])
    start = timeit.default_timer()
    i=0
    for row in rows:
        #try:
        product = GetProductInfo(row[1])
        product_id = product.getProductID()
        product_name = product.getProductName()
        product_brand = product.getProductBrand()
        product_orginal_price = product.getProductOrginalPrice()
        product_selling_price = product.getProductSellingPrice()
        product_discounted_price = product.getProductDiscountedPrice()
        product_rating_count = product.getProductRatingCount()
        product_rating_average = product.getProductAverageRating()
        product_comment_count = product.getProductTotalCommentCount()
        product_favorite_count = product.getProductFavoriteCount()
        seller_name = product.getProductSellerName()
        seller_score = product.getProductSellerScore()
        seller_tax_number  = product.getProductSellerTaxNumber()
        seller_city = product.getProductSellerCityName()
        seller_official_name = product.getProductSellerOfficialName()
        seller_count = product.getProductMerhactCount()
        product_all_sellers = product.getProductAllMerchantNames()
        product_url = product.getProductURL()
        #cursor.execute("INSERT INTO product_details VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (product_id, product_name, product_brand, product_orginal_price,product_selling_price,product_discounted_price,product_rating_count,product_rating_average,product_comment_count,product_favorite_count,seller_name,seller_score,seller_tax_number,seller_city,seller_official_name,seller_count,product_all_sellers,product_url))
        #db.commit()
        satir = {'Ürün ID':product_id, 'Ürün Adı':product_name, 'Marka':product_brand, 'Orjinal Fiyat':product_orginal_price,'Satış Fiyatı':product_selling_price,'İndirimli Fiyat':product_discounted_price,'Değerlendirme Sayısı':product_rating_count,'Değerlendirme Ortalaması':product_rating_average,'Yorum Sayısı':product_comment_count,'Favori Sayısı':product_favorite_count,'Satıcı Adı':seller_name,'Satıcı Puanı':seller_score,'Satıcı Vergi No':seller_tax_number,'Satıcı Şehiri':seller_city,'Satıcı Şirket Adı':seller_official_name,'Ürünü Satan Sayısı':seller_count,'Tüm Satıcılar':product_all_sellers,'Ürün Linki':product_url}
        df = df.append(satir, ignore_index=True)
        #except:
        #    print("error",row)
    db.close()
    stop = timeit.default_timer()
    print('Time: ', stop - start) 
    print(df)
    df.to_excel("output.xlsx") 

product = GetProductInfo("https://www.trendyol.com/kom/kadin-ten-parah-sutyen-p-106815204")
print(product.getProductURL())