import csv
import cloudscraper
from bs4 import BeautifulSoup

def collect_matches(date):
    # Cloudscraper session nesnesi oluşturun
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)

    # URL'yi oluşturun ve istekte bulunun
    url = "https://oddslogs.com/date/{}".format(date)
    response = scraper.get(url)

    # Soup nesnesini oluşturun
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)
    # Tablo içindeki tüm satırları bulun
    table = soup.find("table", class_="table-responsive")
    if table is not None:
        rows = table.find("tbody").find_all("tr")
        # Her satırdaki bilgileri toplayın ve CSV dosyasına yazın
        with open("matches_{}.csv".format(date), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Match", "Date", "League", "Odd 1", "Odd X", "Odd 2"])
            for row in rows:
                cells = row.find_all("td")
                match = cells[0].text.strip()
                date = cells[1].text.strip()
                league = cells[2].text.strip()
                odd_1 = cells[3].text.strip()
                odd_x = cells[4].text.strip()
                odd_2 = cells[5].text.strip()

                writer.writerow([match, date, league, odd_1, odd_x, odd_2])
    else:
        print("No matches found for the specified date.")

    

# Canlı ve bitmiş maçları toplayın
date = "2023-02-10"
collect_matches(date)
