from bs4 import BeautifulSoup
from requests_html import HTMLSession
from rich import print
url = 'https://www.teapuesto.pe/sport/daily-matches'
session = HTMLSession()
html_text = session.get(url)
html_text.html.render()
soup = BeautifulSoup(html_text.html.html, 'lxml')
table = soup.find('div',attrs={'class':'nvs-OddsFilter-list-content-segment-cont'})
print(table)