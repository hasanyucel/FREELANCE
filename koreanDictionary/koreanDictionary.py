import requests,json,timeit
from bs4 import BeautifulSoup
from rich import print
headers = {
  'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Upgrade-Insecure-Requests': '1',
  'DNT': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Cookie': 'STCID=STC2&&TYJvhLvTv0VRy6p4BgqJ5qtxvpHQnsTQStnqZxFTHkF9VjT1wGvZ!582990893!1632169902595; WMONID=GDj_BIx8vZ0; stdict=TYJvhLvTv0VRy6p4BgqJ5qtxvpHQnsTQStnqZxFTHkF9VjT1wGvZ!582990893'
}
data = []
start = timeit.default_timer()
fi = int(input("Please enter first index: "))
li = int(input("Please enter second index: "))
for i in range(fi,li):
    url = f"https://stdict.korean.go.kr/search/popup/wordLink.do?word_no={i}"
    try:
        response = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        word = soup.find('span',attrs={'class':'tit_b'}).text
        try:
            word_type = soup.find('span',attrs={'class':'tit_noun'}).text
            word_type = word_type.replace('\t','').replace('\r','').replace('\n','').strip()
        except:
            word_type = "-"
        meaning = soup.find('p',attrs={'class':'t_number'}).text
        meaning = meaning.replace('\t','').replace('\r','').replace('\n','').replace('「1」','').strip()
        meaning = ' '.join(meaning.split())
        result = {"no":i,"word":word,"word_type":word_type,"meaning":meaning}
        data.append(result)
        print(result)
    except:
        pass
jsonData = {"words":data}
with open("koreanwords"+str(fi)+"-"+str(li)+".json", "w",encoding="utf-8") as outfile:
    json.dump(jsonData, outfile, indent=4, ensure_ascii=False)
stop = timeit.default_timer()
print('Time: ', stop - start) 