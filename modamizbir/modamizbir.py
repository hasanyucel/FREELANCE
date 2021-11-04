import cloudscraper, json, pandas as pd
from rich import print

def getAllProductData(slug):
    url = f"https://api.modamizbir.com/api/v1/product-detail?slug={slug}&lang=tr"
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
    data = scraper.get(url).content
    result = json.loads(data)
    return result

def getLinksFromExcelFile(fileName):
    df = pd.read_excel (f'{fileName}.xlsx')
    return df["Ürün Kodları"]

def getSlugsFromLinks(links):
    slugs = []
    for link in links:
        link = link.replace("https://www.modamizbir.com/","")
        slugs.append(link)
    return slugs

def createExcelData(slugs):
    for slug in slugs:
        productData = getAllProductData(slug)
        productLink = "https://www.modamizbir.com/"+slug
        productId = productData["data"]["id"]
        productName = productData["data"]["UrunAdi"]
        productProperties = productData["data"]["properties"]
        productColor = ""
        for prop in productProperties:
            if prop["ozellik_id"] == 38:
                productColor = prop["TeknikAdi"]
                break
        if productColor == "":
            productColor = "-"
        productOptions = productData["data"]["options"]
        productTotalStock = productData["data"]["StokAdeti"]
        productPrice = float(productData["data"]["Fiyat"]) * (1 + (float(productData["data"]["KdvOrani"])/100))
        productPrice = str(round(productPrice,2)) + " " + productData["data"]["para_birimi_sembol"]
        for option in productOptions:
            productVariant = option["Deger"]
            productStock = option["StokAdeti"]
            print(productLink,productId,productName,productColor,productTotalStock,productVariant,productStock,productPrice)

"""links = getLinksFromExcelFile("urun-kodlari")
slugs = getSlugsFromLinks(links)
print(slugs)"""
slugs = ['mavi-likrali-bayan-askili-pijama-takimi-54623','siyah-fitilli-bayan-tayt-67170','biskuvi-fitilli-bayan-tayt-67171']
createExcelData(slugs)
