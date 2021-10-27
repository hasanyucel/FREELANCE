import requests

url = "https://www.turkiye.gov.tr/buyukcekmece-belediyesi-arsa-rayic-degeri-sorgulama-v2?submit"

payload='mahalle=22979&caddesokak=21224&yil=2021&token=%7B16E5E8-1DE63C-2572FA-5E3FA2-D4DE56-746AE3-E1FD50-7C6349%7D&btn=Sorgula'
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8',
  'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
  'Referer': 'https://www.turkiye.gov.tr/buyukcekmece-belediyesi-arsa-rayic-degeri-sorgulama-v2',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Origin': 'https://www.turkiye.gov.tr/',
  'Connection': 'keep-alive',
  'Cookie': 'TURKIYESESSIONID=eue35pvbkqhgkqfhvhguck2j18; language=tr_TR.UTF-8; w3p=1809033408.20480.0000; TS01ee3a52=015c1cbb6d41ffd20c8023aa7fb808eb1dca66e9ae91fca7d143e11f246561ff19e22efea761b6ff01e970a1d49b4638ceb910c0d4b2bb69bcf1847123f823278f8a00f3cd397f5fa9b60544314594bf749a7cf1fc446705499d23787f34684fce5c9b62ef; top-menu-state=closed; _lastpts=1635242322; _uid=1635242322-8dd53f41-ad2f-49e3-8ad4-776af94188c5; TURKIYESESSIONID=39du3951fs2i0o8il23a7h7d1m; language=tr_TR.UTF-8; TS01ee3a52=015c1cbb6da5672667b8aaa70b784b1e7d307138cb4da57e23c0b216e15c0d5ce32487cb3842c2c998665d75111e7cbe8b17f3659fbcf83d6e3f99520739b156cc27b2a748f9c4156c8af87eaf5c6b612bb1aec1ac7b61e03741cc446fb002db62cf730519; w3p=3822299328.20480.0000',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)