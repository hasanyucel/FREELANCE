import requests, json, regex, sqlite3
from bs4 import BeautifulSoup


database = "veritabani.sqlite"

class GetProducts:
    global data

    def __init__(self,link):
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.find_all("script")[13]
        pattern = '\{(?:[^{}]|(?R))*\}'
        result = regex.search(pattern, str(products)).group(0)
        self.data = json.loads(result)
        db = sqlite3.connect(database)
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS products ('id' TEXT,'url' TEXT,PRIMARY KEY('id'));")
        db.commit()
        db.close()

    def getAllData(self):
        return self.data

    def getTotalProductCount(self):
        return self.data["totalCount"]

    def getAllProductIdUrlToDB(self):
        db = sqlite3.connect(database)
        cursor = db.cursor()
        for i in range (len(self.data["products"])):
            cursor.execute("INSERT OR REPLACE INTO products VALUES (?,?)", (str(self.data["products"][i]["id"]),'https://www.trendyol.com'+self.data["products"][i]["url"]))
        db.commit()
        db.close()
