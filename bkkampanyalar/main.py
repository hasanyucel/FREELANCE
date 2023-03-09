import cloudscraper,json,pandas as pd
from rich import print

df_list = []
i = 1
while True:
    url = f"https://www.bankkart.com.tr/api/Campaigns/GetMoreShow?indexNo={i}&CategoryId=&cuzdan=&arsiv=&type=Bireysel"
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    data = scraper.get(url).text
    data = json.loads(data)
    if not data:
        break
    selected_data = [{'ID': item['Id'], 'Baslik': item['Title'], 'KisaAciklama': item['ShortDescription'], 'BaslangicTarihi': pd.to_datetime(item['StartDate']).strftime('%d/%m/%Y %H:%M:%S'), 'BitisTarihi': pd.to_datetime(item['EndDate']).strftime('%d/%m/%Y %H:%M:%S'), 
                    'Kategori': item['Category']['Title'], 'SonTarih': item['LastDateShow']} for item in data['Items']]
    df = pd.DataFrame(selected_data)
    i += 1
    df_list.append(df)
result_df = pd.concat(df_list, ignore_index=True)   
df = result_df.rename(columns={'Id': 'ID', 'Title': 'Baslik', 'ShortDescription': 'KisaAciklama','StartDate': 'BaslangicTarihi', 'EndDate': 'BitisTarihi','Category': 'Kategori', 'HasCuzdan': 'CuzdanVarMi','DetailSectors': 'DetaySektorler', 'LastDateShow': 'SonTarih'})
print(result_df)
df.to_excel("kampanyalar.xlsx")