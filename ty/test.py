import requests, json, regex, os,re,cloudscraper
from lxml import html
from bs4 import BeautifulSoup
from rich import print

url = f'https://www.trendyol.com/sr?mid=63&pi=3'
scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=50)
data = scraper.get(url).content
soup = BeautifulSoup(data, 'html.parser')
columns = soup.findAll('script', text = re.compile('__SEARCH_APP_INITIAL_STATE__'))[0]
pattern = '\{(?:[^{}]|(?R))*\}'
result = regex.search(pattern, str(columns))[0]
pr = json.loads(result)
for i in range (len(pr["products"])):
    print(i,str(pr["products"][i]["id"]),'https://www.trendyol.com'+ pr["products"][i]["url"])