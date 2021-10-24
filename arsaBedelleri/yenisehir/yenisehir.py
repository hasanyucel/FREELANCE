import cloudscraper
from rich import print

url = "https://www.turkiye.gov.tr/mersin-yenisehir-belediyesi-arsa-rayic-degeri-sorgulama?submit"

payload='btn=Sorgula&caddesokak=3003735&id=&islem=&mahalle=23&token=%7BB83DD6-C84843-6650EB-4D7958-201C49-E65B87-4AB197-D34D8A%7D&yil=2021'
headers = {
  'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Upgrade-Insecure-Requests': '1',
  'DNT': '1',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Cookie': 'TURKIYESESSIONID=hu8gu6l1pfek6d41bnmjioeopf; language=tr_TR.UTF-8; TS01ee3a52=015c1cbb6d4ace793017ae53d8a57df2409ee42c673d531d8a05725d070df91c9c3dad301674d4a3e7a48ac675fa46ff139e9cec2dfc6654383cb82e75035297ec86c7fb3b3cf4c09f9e512ea43e548e0c89d0855d; w3p=2698225856.20480.0000'
}

scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
html = scraper.post(url, data=payload, headers=headers)

print(html.content)
