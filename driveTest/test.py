import pandas as pd
"""licence_key = ""
link = ""
with open('licence.txt') as f:
    licence_key = f.readline().strip()
    link = f.readline().strip()
file_id=link.split('/')[-2]
dwn_url='https://drive.google.com/uc?id=' + file_id
df = pd.read_csv(dwn_url)
row = df.query('account == "tilemountain" & key == "'+licence_key+'"')
tarih = row["tarih"][0]
print(tarih)"""


df = pd.DataFrame({'link':['=HYPERLINK("http://www.google.com", "GOOGLE")']})
df.to_excel('test.xlsx')