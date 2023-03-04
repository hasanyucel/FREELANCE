import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}, delay=10)
url = 'https://www.misterwhat.co.uk/company/2948087-novelli-at-city-quays-belfast'
response = scraper.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

email = ""

email_tag = soup.find('a', {'class': 'show-email'})
if email_tag:
    try:
        email = email_tag.get('href')
    except:
        print("An error occurred while retrieving the email address.")
else:
    print("The 'show email' link was not found.")

print(email)
