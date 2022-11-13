import cloudscraper,pandas,requests
from rich import print
from bs4 import BeautifulSoup

df = pandas.DataFrame(columns=['URL','Kitap Adı','Yazar Adı','Yayın Evi', 'ISBN', 'Fiyat', 'Kategori'])
for i in range(1,2): #(kategorideki sayfa sayısı) + 1 
    url = f'https://www.pandora.com.tr/urunler/genel-muhendislik/133?sayfa={i}'
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    data = scraper.get(url).text
    soup = BeautifulSoup(data,'lxml')
    links = soup.find('ul',attrs={'id':'urunler'})
    links = links.find_all('p',attrs={'class':'edebiyatIsim'})
    
    for link in links:
        kitap_url = link.find('a')
        kitap_url = "https://www.pandora.com.tr" + kitap_url["href"]
        data = scraper.get(kitap_url).text
        soup = BeautifulSoup(data,'lxml')
        detay = soup.find('div',attrs={'id':'urun-detay'})
        kitap_adi = detay.h1.text.strip()
        yazar_adi = detay.find('div',attrs={'class':'col-sm-6 genelBilgiler'}).h2.text.strip()
        yayin_evi = detay.find('div',attrs={'class':'col-sm-6 genelBilgiler'}).p.a.text.strip()
        ISBN = detay.find('div',attrs={'class':'col-sm-6 genelBilgiler'}).p
        ISBN = ISBN.find_next_sibling('p')
        ISBN = ISBN.find_next_sibling('p').text
        ISBN = ISBN.replace('ISBN: ','').strip()
        fiyat = detay.find('div',attrs={'class':'col-sm-6 text-right fiyatBolumu'}).ul.li.strong.text.strip()
        kategori = detay.find('div',attrs={'class':'col-sm-6 genelBilgiler'}).find('p',attrs={'class':'tur'}).a.text.strip()
        satir = {'URL':kitap_url, 'Kitap Adı':kitap_adi,'Yazar Adı':yazar_adi,'Yayın Evi':yayin_evi, 'ISBN':ISBN, 'Fiyat':fiyat, 'Kategori':kategori}
        print(satir)
        df = df.append(satir, ignore_index=True)
df.to_excel("sonuc.xlsx")