import requests, json, regex, sqlite3,re,cloudscraper
from bs4 import BeautifulSoup
from rich import print

database = "veritabani.sqlite"

class GetProducts:
    global data

    def __init__(self,link):
        print(link)
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=50)
        data = scraper.get(link).content
        soup = BeautifulSoup(data, 'html.parser')
        products = soup.findAll('script', text = re.compile('__SEARCH_APP_INITIAL_STATE__'))
        pattern = '\{(?:[^{}]|(?R))*\}'
        result = regex.search(pattern, str(products[0]))[0]
        self.data = json.loads(result)

    def getAllData(self):
        return self.data

    def getTotalProductCount(self):
        return self.data["totalCount"]

    def getAllProductIdUrlToDB(self):
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS products ('id' TEXT,'url' TEXT,PRIMARY KEY('id'));")
        db.commit()
        for i in range (len(self.data["products"])):
            print(i,str(self.data["products"][i]["id"]),'https://www.trendyol.com'+ self.data["products"][i]["url"])
            cursor.execute("INSERT OR REPLACE INTO products VALUES (?,?)", (str(self.data["products"][i]["id"]),'https://www.trendyol.com'+self.data["products"][i]["url"]))
        db.commit()
        db.close()
