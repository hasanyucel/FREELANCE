import requests, json, regex, os,re
from lxml import html
from bs4 import BeautifulSoup
from rich import print

link = "https://www.trendyol.com/merry-secret-s/kadin-dantelli-dolgulu-sutyen-p-57438714"
r = requests.get(link)
soup = BeautifulSoup(r.text, 'html.parser')
nf = soup.find("h1")
#columns = soup.findAll('script', text = re.compile('__PRODUCT_DETAIL_APP_INITIAL_STATE__'))
print(nf)