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
    
    if  'latitude' in json_object["geo"]:
        latitude = json_object["geo"]["latitude"]
    else:
        latitude = '-'

    if  'longitude'in json_object["geo"]:
        longitude = json_object["geo"]["longitude"]
    else:
        longitude = '-'
    
    if  'telephone' in json_object:
        telephones = json_object["telephone"]
        if type(telephones) is list:
            telephones = ';'.join(telephones)
    else:
        telephones = '-'

    if  'faxNumber' in json_object:
        faxNumber = json_object["faxNumber"]
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
    #print('priceRange : ',priceRange)

print("Script is working...")
t0 = time.time()
#createDbAndTables()
#insert sitemap link https://www.dasschnelle.at/sitemaps/dasschnelle-at/detail_sitemap_customers-1.xml
#insert sitemap link https://www.dasschnelle.at/sitemaps/dasschnelle-at/detail_sitemap_customers-2.xml

#urls = getTableColumn('SiteMapLinks','Url')
#for url in urls: 
#    insertAllLinks(url,'SiteLinks')
error_links = []
counter = 1
urls = getTableColumn('SiteLinks','Url')

for url in urls:
    if counter % 20 == 0:
        sleep(120)
    try:
        print(counter, url)
        getIdentityDetails(url)
        counter+=1
    except:
        print('ERROR -------- ',url)
        error_links.append(url)
        pass

print(error_links)
#while len(error_links) == 0:
#
#    for url in error_links:
#        if counter % 20 == 0:
#            sleep(120)
#        try:
#            print(counter, url)
#            getIdentityDetails(url)
#            error_links.remove(url)
#            counter+=1
#        except:
#            error_links.append(url)
#            pass


#getIdentityDetails('https://www.dasschnelle.at/reinisch-gesmbh-feldbach-mühldorfer-straße') #https://www.dasschnelle.at/blumen-egerth-exenberger-renate-kufstein-gewerbehof

t1 = time.time()
print(f"{t1-t0} seconds.")


#    'https://www.dasschnelle.at/stadtgemeinde-baden-baden-hauptplatz',
#    'https://www.dasschnelle.at/mag-claudia-schmidt-psychotherapeutin-i-a-u-s-bad-ischl-wiesingerstraße',
#    'https://www.dasschnelle.at/freizeitanlage-schlögen-e-u-pächter-andrea-winkler-moos-mitterberg',
#    'https://www.dasschnelle.at/saringer-gmbh-schwaz-gewerbepark-einfang',
#    'https://www.dasschnelle.at/rauch-steuerberatung-gesmbh-steinach-zirmweg',
#    'https://www.dasschnelle.at/a-hechenblaikner-versicherungsmakler-gmbh-reutte-planseestraße',
#    'https://www.dasschnelle.at/haselsberger-markus-lähn-unterdorf',
#    'https://www.dasschnelle.at/entfeuchtungstechnik-gruber-breitenwang-unterried',
#    'https://www.dasschnelle.at/wegmann-wolfgang-dr-ehrwald-kirchplatz',
#    'https://www.dasschnelle.at/unser-lagerhaus-warenhandelsgesmbh-ötztal-bahnhof-handelsweg',
#    'https://www.dasschnelle.at/hassel-peter-ötztal-bahnhof-bahnrain',
#    'https://www.dasschnelle.at/architec-zt-gesmbh-wolfsberg-johann-offner-straße',
#    'https://www.dasschnelle.at/schneeberger-gmbh-atzbach-hauptstraße',
#    'https://www.dasschnelle.at/hölblinger-und-zefferer-hoch-u-tiefbau-gesmbh-mariazell-bundesstraße',
#    'https://www.dasschnelle.at/stadtgemeinde-bruck-an-der-mur-bruck-an-der-mur-koloman-wallisch-platz',
#    'https://www.dasschnelle.at/kaiblinger-rechtsanwalts-gmbh-gunskirchen-marktplatz',
#    'https://www.dasschnelle.at/umlauft-schuhhaus-neumarkt-am-wallersee-hauptstraße',
#    'https://www.dasschnelle.at/apotheke-st-mang-füssen-reichenstr',
#    'https://www.dasschnelle.at/ausbildungszentrum-braunau-braunau-industriezeile',
#    'https://www.dasschnelle.at/hohner-sabrina-traun-hauptplatz',
#    'https://www.dasschnelle.at/schloss-traun-traun-schlossstraße',
#    'https://www.dasschnelle.at/tscharnuter-bau-gmbh-verputzarbeiten-ehrwald-schanz',
#    'https://www.dasschnelle.at/mobile-säge-florian-haas-kitzbühel-fichterfeld',
#    'https://www.dasschnelle.at/nagler-bau-gmbh-ternberg-dürnbachstraße',
#    'https://www.dasschnelle.at/as-installationen-braunau-am-inn-mattighofner-straße',
#    'https://www.dasschnelle.at/arnaut-alma-braunau-am-inn-mattighofner-straße',
#    'https://www.dasschnelle.at/check-er-fitness-gmbh-simbach-kreuzberger-weg',
#    'https://www.dasschnelle.at/schmidhammer-wolfgang-salzburg-vogelweiderstraße',
#    'https://www.dasschnelle.at/kink-erich-baden-kaiser-franz-joseph-ring',
#    'https://www.dasschnelle.at/stadtgemeinde-baden-baden-neustiftgasse',
#    'https://www.dasschnelle.at/ahammer-karl-altmünster-maria-theresiastr',
#    'https://www.dasschnelle.at/frauenhaus-ried-ried-im-innkreis-postfach',
#    'https://www.dasschnelle.at/pacher-wolfgang-gmünd-dornbach',
#    'https://www.dasschnelle.at/leitner-günter-öhling-im-reith',
#    'https://www.dasschnelle.at/haider-klemens-dr-attnang-puchheim-römerstraße',
#    'https://www.dasschnelle.at/kaspar-gudrun-dr-klosterneuburg-hauptstraße',
#    'https://www.dasschnelle.at/strauss-c-dr-vöcklamarkt-hauptstraße',
#    'https://www.dasschnelle.at/der-steinacher-ramsau-hoferstraße',
#    'https://www.dasschnelle.at/ddr-peter-zwittnig-straßengel-plankenwartherstraße',
#    'https://www.dasschnelle.at/oä-dr-waltraud-stromer-horn-ing-karl-proksch-gasse',
#    'https://www.dasschnelle.at/dr-peter-vlasak-3-cz-studanky-cz-studanky',
#    'https://www.dasschnelle.at/carta-büro-u-kopiertechnik-gmbh-sankt-johann-im-pongau-hauptstraße',
#    'https://www.dasschnelle.at/mag-katharina-höchtl-kronheim-ottensheim-hostauerstraße',
#    'https://www.dasschnelle.at/raiffeisen-lagerhaus-lavanttal-reggenmbh-wolfsberg-tanglstraße',
#    'https://www.dasschnelle.at/maschinenring-hollabrunn-horn-mold-mold',
#    'https://www.dasschnelle.at/klingelbrunner-ernst-jun-baumgarten-am-tullnerfeld-hauptstraße',
#    'https://www.dasschnelle.at/robert-köppel-fenster-türen-sonnenschutz-gmbh-gratwein-straßengel-murfeldstraße',
#    'https://www.dasschnelle.at/innenbau-peschel-gmbh-groß-siegharts-reiterweg',
#    'https://www.dasschnelle.at/aigner-optiker-gmbh-grieskirchen-oberer-stadtplatz',
#    'https://www.dasschnelle.at/kräuterpfarrer-zentrum-verein-freunde-der-heilkräuter-karlstein-an-der-thaya-hauptstraße',
#    'https://www.dasschnelle.at/georg-und-gabriele-stocker-ohg-kies-u-fertigbetonwerk-transport-neuhaus-redinger-straße',
#    'https://www.dasschnelle.at/pfeiler-s-flug-reisen-gmbh-simbach-innstraße',
#    'https://www.dasschnelle.at/tischberger-christian-dr-laussa-kirchenplatz',
#    'https://www.dasschnelle.at/marker-erich-gesmbh-und-co-kg-pottenstein-bundesstraße',
#    'https://www.dasschnelle.at/gasthof-pension-göttler-simbach-pfarrkirchner-straße',
#    'https://www.dasschnelle.at/dr-bernhard-distlbacher-gmünd-stadtplatz',
#    'https://www.dasschnelle.at/zirngast-kfz-ges-m-b-h-nfg-kg-leibnitz-grazer-straße',
#    'https://www.dasschnelle.at/robert-pomberger-mariazell-friedhofgasse',
#    'https://www.dasschnelle.at/notariat-schärding-schärding-innere-stadt-innbruckstraße',
#    'https://www.dasschnelle.at/riedl-bau-marchtrenk-nelkenstraße',
#    'https://www.dasschnelle.at/volkshochschule-baden-baden-johannesgasse',
#    'https://www.dasschnelle.at/zirngast-kfz-gmbh-nfg-keg-neutillmitsch-grazerstrasse',
#    'https://www.dasschnelle.at/malermeister-pils-gmbh-freistadt-schützengasse'