import cloudscraper
from rich import print
from bs4 import BeautifulSoup

run = False
match_count = 0
link_count = 0
db = "oddlogs.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'MatchDetails' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    cur.execute("CREATE TABLE IF NOT EXISTS 'MatchOdds' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    conn.commit()
    conn.close()

def getLinks(i=1):
    url = f'https://oddslogs.com/?page={i}'
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    data = scraper.get(url).text
    soup = BeautifulSoup(data,'lxml')
    global run,match_count,link_count
    if not run:
        run = True
        c_object = soup.find('div',attrs={'class':'p-md-3'}) #ilk sayfandan maç sayısı alır
        c_object = c_object.find('a').text
        find_match_count = c_object.split()
        find_match_count = find_match_count[0].strip()
        match_count = int(find_match_count)

    links = soup.find_all('a',attrs={'class':'match__event'})
    
    for link in links:
        a = 'https://oddslogs.com'+link['href']
        link_count += 1
        print(link_count,a)
    
    page_num = match_count / 150
    print(url) 
    if page_num > i:  #eğer sayfa varsa recursive olarak fonksiyonu çağırıyor.
        i += 1 
        getLinks(i)

#getLinks()
def getDetails(link):
    match_id = link.split('/')
    match_id = match_id[4]
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    data = scraper.get(link).text
    soup = BeautifulSoup(data,'lxml')
    date_time_league = soup.find('div',attrs={'class':'card-header'})
    date =  date_time_league.find('span',attrs={'class':'view-date text-end text-wrap'}).text
    date = date.split(' - ')
    time = ' '.join(date[1].split()) #Saat
    date = date[0] #Tarih
    league =  date_time_league.find('h2',attrs={'d-inline'}).text
    league = ' '.join(league.split()) #Lig
    team_home = soup.find('div',attrs={'class':'col-md-5 col-4 text-center team-home'}).h4.text #Ev Sahibi
    team_away = soup.find('div',attrs={'class':'col-md-5 col-4 text-center team-away'}).h4.text #Deplasman
    ft = soup.find('div',attrs={'class':'fw-bolder fs-3'}).text
    ft = ' '.join(ft.split()) #FT
    details = soup.find('div',attrs={'class':'d-flex justify-content-between flex-wrap'}) 
    heat = details.find('span').text.strip()
    weather = details.find('span').find_next('span').text.strip()
    wind = details.find('span').find_next('span').find_next('span').find_next('span').text.strip()
    pressure = details.find('span').find_next('span').find_next('span').find_next('span').find_next('span').find_next('span').text.strip()
    humidity = details.find('span').find_next('span').find_next('span').find_next('span').find_next('span').find_next('span').find_next('span').find_next('span').text.strip()
    football_field = details.find('div',attrs = {'class':'d-none d-md-inline'}).text.strip()
    statitics = soup.find('div', attrs= {'class':'card-body match-stat px-3'})
    statitics = statitics.find_all('div', attrs= {'class':'mb-2'})
    home_attack = statitics[0].find('div', attrs= {'class':'progress-bar bg-primary'}).text
    away_attack = statitics[0].find('div', attrs= {'class':'progress-bar bg-success'}).text
    home_dan_attack = statitics[1].find('div', attrs= {'class':'progress-bar bg-primary'}).text
    away_dan_attack = statitics[1].find('div', attrs= {'class':'progress-bar bg-success'}).text
    sont_home = statitics[3].find('div', attrs= {'class':'progress-bar bg-primary'}).text
    sont_away = statitics[3].find('div', attrs= {'class':'progress-bar bg-success'}).text
    soft_home = statitics[4].find('div', attrs= {'class':'progress-bar bg-primary'}).text
    soft_away = statitics[4].find('div', attrs= {'class':'progress-bar bg-success'}).text
    corner_home = statitics[5].find('div', attrs= {'class':'progress-bar bg-primary'}).text
    corner_away = statitics[5].find('div', attrs= {'class':'progress-bar bg-success'}).text
    table = soup.find('table')
    trs = table.find_all('tr')
    print(team_home,team_away)
    print(heat,weather,wind,pressure,humidity,football_field)
    print(date,time)
    for i in range(1,len(trs)):
        minute = trs[i].th.text.replace('\'','')
        tds = trs[i].find_all('td')
        score = tds[0].text
        t_1 = tds[1].text
        t_x = tds[2].text
        t_2 = tds[3].text
        t_1x = tds[4].text
        t_12 = tds[5].text
        t_x2 = tds[6].text
        t_hcap1 = tds[7].text
        t_hcap1 = ' '.join(t_hcap1.split())
        t_hc1 = tds[8].text
        t_hcap2 = tds[9].text
        t_hcap2 = ' '.join(t_hcap2.split())
        t_hc2 = tds[10].text
        t_total = tds[11].text
        t_O = tds[12].text
        t_U = tds[13].text
        #print(match_id, minute,score,t_1,t_x,t_2,t_1x,t_12,t_x2,t_hcap1,t_hc1,t_hcap2,t_hc2,t_total,t_O,t_U)


getDetails("https://oddslogs.com/match/247539/world-belgium-morocco")



