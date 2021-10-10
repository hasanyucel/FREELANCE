import cloudscraper,json,html,time,pandas,requests
yazar = "fyodor-dostoyevski"
df = pandas.DataFrame(columns=['Kitap','Söz'])
for i in range(0,101):
    url = f'https://api.1000kitap.com/yazarCekV2?id={yazar}&bolum=alintilar&sayfa={i}'
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    byte_data = scraper.get(url).content
    json_data = json.loads(byte_data)
    for j in range(0,10):
        try:
            soz = html.unescape(json_data['gonderiler'][j]['alt']['sozler']['soz'])
            kitap = html.unescape(json_data['gonderiler'][j]['alt']['kitaplar']['adi'])
            satir = {'Kitap':kitap, 'Söz':soz}
            print(satir)
            df = df.append(satir, ignore_index=True)
        except:
            pass
df.to_excel(f"{yazar}.xlsx")