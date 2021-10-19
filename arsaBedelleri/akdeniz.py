from bs4 import BeautifulSoup
import requests,json
from rich import print

r = requests.get("https://e-belediye.akdeniz.bel.tr/tr-tr/emlak/arsa-birim-degerleri")

def getYillar():
    soup = BeautifulSoup(r.content, 'html.parser')
    yillar_html = soup.find("select",attrs={'id':'yil'})
    yillar_select = yillar_html.find_all("option")
    yillar = []
    for yil in yillar_select:
        yillar.append(yil.text)
    return yillar

def getMahalleler():
    soup = BeautifulSoup(r.content, 'html.parser')
    mahalleler_html = soup.find("select",attrs={'id':'MahalleId'})
    mahalleler_select = mahalleler_html.find_all("option") #ilk iki value gereksiz
    mahalleler = []
    for mahalle in mahalleler_select:
        mahalleler.append(mahalle['value'])
        print(mahalle['value'],mahalle.text)
    return mahalleler

def getCaddeSokaklar(mahalleKodu):
    url = f"https://e-belediye.akdeniz.bel.tr/tr-tr/cadde-sokak?mahalleKodu={mahalleKodu}"
    headers = {
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': 'ASP.NET_SessionId=vixgacpnaan3mzxdg5jzbqyj; Culture=tr-tr'
    }
    response = requests.request("GET", url, headers=headers)
    result = json.loads(response.text)
    SonucAciklamasi = result["SonucAciklamasi"]
    print(SonucAciklamasi)
    CaddeSokaklar = result["CaddeSokaklar"]
    caddeler = []
    for cadde in CaddeSokaklar:
        if cadde["CaddeSokakKodu"] != 0:
            caddeler.append(cadde["MahalleId"])
    return caddeler

#caddeler = getCaddeSokaklar("996")
yillar = getYillar()
mahalleler = getMahalleler()
print(mahalleler)