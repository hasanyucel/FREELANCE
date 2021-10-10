import requests,sqlite3,json,timeit
from bs4 import BeautifulSoup
from rich import print
import requests

data = []
headers = {
  'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'DNT': '1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document'
}
i = 1
start = timeit.default_timer()
with open("linkler.txt") as file:
    for line in file:
        url = line.rstrip()
        response = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        word = soup.find('h1',attrs={'class':'dwdswb-ft-lemmaansatz'})
        if word is not None:
            word = word.b
            if word is not None:
                word = word.text
            else:
                word = None
        else:
            word = None
        kategoriler = soup.find('span',attrs={'class':'dwdswb-ft-blocktext'})
        if kategoriler is not None:
            kategoriler = kategoriler.text
            kategoriler = kategoriler.split(' · ')
        else:
            kategoriler = None
        anlamlar = soup.find('span',attrs={'class':'dwdswb-definitionen'})
        if anlamlar is not None:
            anlamlar = anlamlar.text
        else:
            try:
                anlamlar = soup.select("body > main > div > div > div.col-md-9.article-leftcol > div:nth-child(2) > div > div.dwds-gb-list > div:nth-child(1) > div.sans")[0].text
                anlamlar = "Ex: " + anlamlar
            except IndexError:
                anlamlar = "No Meaning or Example"
        #result = {word:{"anlamlar":anlamlar,"kategoriler":kategoriler,"url":url}}
        result = {word:{"anlamlar":anlamlar,"kategoriler":kategoriler}}
        data.append(result)
        print(str(i)+ " - " +str(result))
        if i%5000==0:
            jsonData = data
            with open("germanwords_"+str((i-4999))+"-"+str(i)+".json", "w",encoding="utf-8") as outfile:
                json.dump(jsonData, outfile, indent=4, ensure_ascii=False)
            data = []
        i=i+1
jsonData = data
with open("germanwords_"+str(i-1)+".json", "w",encoding="utf-8") as outfile:
    json.dump(jsonData, outfile, indent=4, ensure_ascii=False)
stop = timeit.default_timer()
print('Time: ', stop - start) 