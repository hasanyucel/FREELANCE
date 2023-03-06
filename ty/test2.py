import requests
import cloudscraper,pandas,requests
from rich import print
from bs4 import BeautifulSoup

url = "https://public-mdc.trendyol.com/discovery-sellerstore-webgw-service/v1/ugc/product-reviews/reviews/104929?page=0&size=50&isMarketplaceMember=true"
scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
data = scraper.get(url).text
soup = BeautifulSoup(data,'lxml')
print(data)
#
#payload={}
#headers = {
#  'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
#  'DNT': '1',
#  'sec-ch-ua-mobile': '?0',
#  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
#  'sec-ch-ua-platform': '"Windows"',
#  'Accept': '*/*',
#  'host': 'public-mdc.trendyol.com',
#  'Cookie': 'SearchMode=1; VisitCount=1; WebAbTesting=A_93-B_56-C_44-D_5-E_66-F_96-G_78-H_63-I_2-J_87-K_23-L_14-M_27-N_61-O_24-P_26-Q_32-R_76-S_17-T_29-U_47-V_83-W_64-X_90-Y_46-Z_8; __cfruid=81e59a6166ea46f6d649f25865f25f9f4c6b4ccd-1678126408; _cfuvid=j8WM05.BuWWFqIKSCpPFq8KOMIX6oll4R_uLXhKEoZU-1678126408059-0-604800000; hvtb=1; platform=web; __cflb=02DiuHfCEPukG5vqapgzTKyFWDC2x7LVau9MthmPf1HRv'
#}
#
#response = requests.request("GET", url, headers=headers, data=payload)
#
#print(response.text)
