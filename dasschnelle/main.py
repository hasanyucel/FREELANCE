import cloudscraper,pandas,time,sqlite3,json
from rich import print
from bs4 import BeautifulSoup
from bs2json import bs2json
from time import sleep

db = "dasschnelle.sqlite"

def createDbAndTables():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteMapLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    cur.execute("CREATE TABLE IF NOT EXISTS 'SiteLinks' ('Url' TEXT NOT NULL,PRIMARY KEY('Url'));")
    cur.execute("CREATE TABLE IF NOT EXISTS 'Identities' ('link' TEXT NOT NULL, 'name' TEXT,'description' TEXT, 'streetAddress' TEXT, 'postalCode' TEXT, 'addressLocality' TEXT, 'addressRegion' TEXT, 'addressCountry' TEXT, 'latitude' TEXT, 'longitude' TEXT, 'telephones' TEXT, 'faxNumber' TEXT, 'email' TEXT, 'urls' TEXT, 'logo' TEXT, 'images' TEXT, 'priceRange' TEXT, PRIMARY KEY('link') );")
    conn.commit()

def insertAllLinks(xml,table_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=10)
    r = scraper.get(xml)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text, 'lxml')
    urls = [loc.string for loc in soup.find_all('loc')]
    for url in urls:
        cur.execute(f"INSERT OR IGNORE INTO {table_name} (URL) VALUES (?)",(url,))
    conn.commit()
    conn.close()

def getTableColumn(table_name,column_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f'SELECT {column_name} FROM {table_name}')
    links = cur.fetchall()
    links = [f[0] for f in links]
    conn.close()
    return links

def insertData(link,name,description,streetAddress,postalCode,addressLocality,addressRegion,addressCountry,latitude,longitude,\
        telephones,faxNumber,email,urls,logo,images,priceRange):
    
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"INSERT OR REPLACE INTO Identities (link,name,description,streetAddress,postalCode,addressLocality,addressRegion,addressCountry,latitude,longitude,\
        telephones,faxNumber,email,urls,logo,images,priceRange) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(link,name,description,streetAddress,postalCode,addressLocality,addressRegion,addressCountry,latitude,longitude,\
        telephones,faxNumber,email,urls,logo,images,priceRange))
    conn.commit()
    conn.close()

def getIdentityDetails(link):
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},delay=200)
    r = scraper.get(link)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text,'lxml')
    json_tag = soup.find_all('script',attrs={'type':'application/ld+json'})
    
    converter = bs2json()
    json_ = converter.convertAll(json_tag,join=True)
    data = json_[0]['script'][-1]['text']
    json_object = json.loads(data, strict=False)
    if 'name' in json_object:
        name = json_object["name"]
    else:
        name = '-'
    
    if 'description' in json_object:
        description = json_object["description"]
    else:
        description = '-'
    
    if 'streetAddress' in json_object["address"]:
        streetAddress = json_object["address"]["streetAddress"]
    else:
        streetAddress = '-'

    if 'postalCode' in json_object["address"]:
        postalCode = json_object["address"]["postalCode"]
    else:
        postalCode = '-'

    if 'addressLocality' in json_object["address"]:
        addressLocality = json_object["address"]["addressLocality"]
    else:
        addressLocality = '-'
    
    if 'addressRegion' in json_object["address"]:
        addressRegion = json_object["address"]["addressRegion"]
    else:
        addressRegion = '-'
    
    if  'addressCountry' in json_object["address"]:
        addressCountry = json_object["address"]["addressCountry"]
    else:
        addressCountry = '-'

    if  'geo' in json_object:    

        if  'latitude' in json_object["geo"]:
            latitude = json_object["geo"]["latitude"]
        else:
            latitude = '-'

        if  'longitude'in json_object["geo"]:
            longitude = json_object["geo"]["longitude"]
        else:
            longitude = '-'
    
    else:
        latitude = '-'
        longitude = '-'
    
    if  'telephone' in json_object:
        telephones = json_object["telephone"]
        if type(telephones) is list:
            telephones = ';'.join(telephones)
    else:
        telephones = '-'

    if  'faxNumber' in json_object:
        faxNumber = json_object["faxNumber"]
        if type(faxNumber) is list:
            faxNumber = ';'.join(faxNumber)
    else:
        faxNumber = '-'

    if  'email' in json_object:
        email = json_object["email"]
        if type(email) is list:
            email = ';'.join(email)
    else:
        email = '-'

    if  'url' in json_object:
        urls = json_object["url"]
        if type(urls) is list:
            urls = ';'.join(urls)
    else:
        urls = '-'
    
    if  'logo' in json_object:
        logo = json_object["logo"]
    else:
        logo = '-'
    
    if  'image' in json_object:
        images = json_object["image"]
        if type(images) is list:
            images = ';'.join(images)
    else:
        images = '-'

    if  'priceRange' in json_object:
        priceRange = json_object["priceRange"]
    else:
        priceRange = '-'
    
    insertData(link,name,description,streetAddress,postalCode,addressLocality,addressRegion,addressCountry,latitude,longitude,\
        telephones,faxNumber,email,urls,logo,images,priceRange)
    print(name)
    #print('name : ',name)
    #print('description : ',description)
    #print('streetAddress : ',streetAddress)
    #print('postalCode : ',postalCode)
    #print('addressLocality : ',addressLocality)
    #print('addressRegion : ',addressRegion)
    #print('addressCountry : ',addressCountry)
    #print('latitude : ',latitude)
    #print('longitude : ',longitude)
    #print('telephones : ',telephones)
    #print('faxNumber : ',faxNumber)
    #print('email : ',email)
    #print('urls : ',urls)
    #print('logo : ',logo)
    #print('images : ',images)
    print('priceRange : ',priceRange)

print("Script is working...")
t0 = time.time()
#createDbAndTables()
#insert sitemap link https://www.dasschnelle.at/sitemaps/dasschnelle-at/detail_sitemap_customers-1.xml
#insert sitemap link https://www.dasschnelle.at/sitemaps/dasschnelle-at/detail_sitemap_customers-2.xml

#urls = getTableColumn('SiteMapLinks','Url')
#for url in urls: 
#    insertAllLinks(url,'SiteLinks')
#error_links = []
#counter = 1
#urls = getTableColumn('SiteLinks','Url')
#
#for url in urls:
#    if counter % 20 == 0:
#        sleep(120)
#    try:
#        print(counter, url)
#        getIdentityDetails(url)
#        counter+=1
#    except:
#        print('ERROR -------- ',url)
#        error_links.append(url)
#        pass
#
#print(error_links)

#for link in error_links:
#    getIdentityDetails(link) #https://www.dasschnelle.at/blumen-egerth-exenberger-renate-kufstein-gewerbehof

t1 = time.time()
print(f"{t1-t0} seconds.")