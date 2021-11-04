import cloudscraper
import json
from rich import print
import pandas as pd


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

links = getLinksFromExcelFile("urun-kodlari")
slugs = getSlugsFromLinks(links)
print(slugs)
"""productData = getAllProductData(slug)
print(productData)"""