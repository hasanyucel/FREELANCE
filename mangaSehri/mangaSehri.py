import cloudscraper

url = f'https://mangasehri.com/manga/'
scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
data = scraper.get(url).content
print(data)

