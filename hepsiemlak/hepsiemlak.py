import cloudscraper, json
from rich import print

def getAllSaleData():
    url = f"https://www.hepsiemlak.com/api/realty-list/ankara-satilik?&fillIntentUrls=false"
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
    data = scraper.get(url).content
    result = json.loads(data)
    return result["realtyList"][0]

print(getAllSaleData())