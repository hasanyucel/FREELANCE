import requests, json, regex, os,re,cloudscraper
from lxml import html
from bs4 import BeautifulSoup
from rich import print

def get_seller_id(url):
    start_index = url.find("mid=") + 4
    end_index = url.find("&", start_index)
    if end_index == -1: # eğer '&' işareti yoksa end_index -1 olacaktır
        seller_id = url[start_index:]
    else:
        seller_id = url[start_index:end_index]
    return seller_id

def get_all_product_comments(seller_id):
    url = f"https://public-mdc.trendyol.com/discovery-sellerstore-webgw-service/v1/ugc/product-reviews/reviews/{seller_id}?page=0&size=1&isMarketplaceMember=true"
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    data = scraper.get(url).text
    data = json.loads(data)
    total_pages = data["productReviews"]["totalPages"]
    print(data)
    

seller_id = get_seller_id("https://www.trendyol.com/sr?mid=63")
print(seller_id)
get_all_product_comments(seller_id)

#import datetime
#
#unix_timestamp = 1676703842621 / 1000  # milisaniyeleri saniyelere çeviriyoruz
#date = datetime.datetime.fromtimestamp(unix_timestamp)
#
#print(date.strftime('%d/%m/%Y %H:%M:%S'))

#url = f'https://www.trendyol.com/sr?mid=63&pi=3'
#scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=50)
#data = scraper.get(url).content
#soup = BeautifulSoup(data, 'html.parser')
#columns = soup.findAll('script', text = re.compile('__SEARCH_APP_INITIAL_STATE__'))[0]
#pattern = '\{(?:[^{}]|(?R))*\}'
#result = regex.search(pattern, str(columns))[0]
#pr = json.loads(result)
#for i in range (len(pr["products"])):
#    print(i,str(pr["products"][i]["id"]),'https://www.trendyol.com'+ pr["products"][i]["url"])




