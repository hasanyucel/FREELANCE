import time,sqlite3,concurrent.futures,cloudscraper
from bs4 import BeautifulSoup
from rich import print

db = 'crunchbase.db'

def create_db_objects():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS base_urls (
                        id INTEGER PRIMARY KEY,
                        url TEXT);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS funding_round_overview (
                        url TEXT,
                        key TEXT,
                        value TEXT,
                        UNIQUE(url, key));''')
    conn.commit()
    conn.close()

def insert_funding_round_overview_data(url, key, value):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO funding_round_overview (url, key, value) VALUES (?, ?, ?)', (url, key, value))
    conn.commit()
    conn.close()

def process_funding_round_overview_data(soup, url):
    ul = soup.find('ul', {'class': 'text_and_value'})
    print(ul)
    for li in ul.find_all('li'):
        key = li.find('span').text.strip()
        value = li.find('field-formatter').text.strip()
        print(key,value)
        insert_funding_round_overview_data(url, key, value)

def scrape_data(url):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}, delay=10)
    data = scraper.get(url)
    soup = BeautifulSoup(data.content, 'html.parser')
    print(soup)
    process_funding_round_overview_data(soup, url)

urls = [
    'https://www.crunchbase.com/funding_round/jamdatmobile-series-c--a9ccaff2',
    'https://www.crunchbase.com/funding_round/janalakshmi-series-c--a1c41981'
]

create_db_objects()
scrape_data("https://www.crunchbase.com/funding_round/jamdatmobile-series-c--a9ccaff2")
#with concurrent.futures.ThreadPoolExecutor() as executor:
#    futures = [executor.submit(scrape_data, url) for url in urls]