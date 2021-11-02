import requests, json, regex, os,re
from lxml import html
from bs4 import BeautifulSoup
from rich import print

link = "https://www.trendyol.com/raymond-weil/erkek-kol-saati-7830-bk-05207-p-31105018"
r = requests.get(link)
soup = BeautifulSoup(r.text, 'html.parser')
columns = soup.findAll('script', text = re.compile('__PRODUCT_DETAIL_APP_INITIAL_STATE__'))
print(columns[0])