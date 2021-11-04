import cloudscraper, json, pandas as pd
from rich import print

def makeHyperlink(url):
    return f'=Hyperlink("{url}","Ürün")'

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
    df = pd.DataFrame(columns=['Link','Ürün ID','Ürün Adı','Renk','Toplam Stok','Beden','Stok','Fiyat'])
    for slug in slugs:
        productData = getAllProductData(slug)
        productLink = "https://www.modamizbir.com/"+slug
        if productData["status"] != 0:
            productId = productData["data"]["id"]
            productName = productData["data"]["UrunAdi"]
            productName = productName.rsplit(' ', 1)[0]
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
                productStock = int(option["StokAdeti"])
                print(productLink,productId,productName,productColor,productTotalStock,productVariant,productStock,productPrice)
                satir = {'Link':productLink,'Ürün ID':productId,'Ürün Adı':productName,'Renk':productColor,'Toplam Stok':productTotalStock,'Beden':productVariant,'Stok':productStock,'Fiyat':productPrice}
                df = df.append(satir, ignore_index=True)
        else:
            print(productLink, " linkinde ürün bulunamadı!")
    saveExcel(df)

def saveExcel(df):
    df['Link'] = df.apply(lambda row : makeHyperlink(row['Link']), axis = 1)
    writer = pd.ExcelWriter('stok-bilgisi.xlsx')  
    df.to_excel(writer, sheet_name='modamizbir', index=False, na_rep='NaN')
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['modamizbir'].set_column(col_idx, col_idx, column_width+1)
    col_idx = df.columns.get_loc('Link')
    writer.sheets['modamizbir'].set_column(col_idx, col_idx, 10)
    writer.save() 

#links = getLinksFromExcelFile("urun-kodlari")
#slugs = getSlugsFromLinks(links)
#print(slugs)
slugs = ['mavi-likrali-bayan-askili-pijama-takimi-54623','siyah-fitilli-bayan-tayt-67170','biskuvi-fitilli-bayan-tayt-67171']
createExcelData(slugs)
