import requests,random,string,json,sqlite3,os,unidecode
from rich import print
from dotenv import load_dotenv
load_dotenv()

username = "hasanyucel"
token = os.getenv('name_api_token')
db_name = "db"
table_name = "fiveletterdomains"
dom_ext = ".com"
f_ext = ".txt"


def readDomainsFromTXT(path): #TXT dosyalarındaki satırları .com listesi olarak döner.
    domains = []
    f = open(path,'r') #'__location__+\kelime\A.txt'
    for line in f:
        line = unidecode.unidecode(line.strip())
        line = line.replace(' ','').lower()
        domains.append(line+dom_ext)
    return domains

def createRandomDomainList(size): #Apinin tek sorguda sorgulayacağı maximum adette random n-size domain listesini hazırlar
    domains = []
    for j in range(50):
        domains.append(random_nletter_domain_name_generator(size=size)+dom_ext)
    return domains

def random_nletter_domain_name_generator(size=6, chars=string.ascii_lowercase):#Random domain oluşturmaya yarar.
    return ''.join(random.choice(chars) for _ in range(size))

def checkDomains(username,token,domains,db_name,table_name): #Api kullanarak domainlerin durumunlarını kontrol eder. 
    controlDbTable(db_name,table_name) 
    while(len(domains)>50): 
        response = getNameApiResult(username,token,domains)
        print(response)
    if(len(domains)<=50):
        response = getNameApiResult(username,token,domains)
    irdDatabase(db_name,response["results"])

def getNameApiResult(username,token,domains): #Name API ile sorgulama sonuçlarını döndürür. 
    headers = {'Content-Type': 'application/json',}
    temp = []
    for i in range(len(domains)):
        temp.append(domains.pop(0))
    data = json.dumps({"domainNames": temp})
    response = requests.post('https://api.name.com/v4/domains:checkAvailability', headers=headers, data=data, auth=(username, token)).content.decode()
    return json.loads(response)

def controlDbTable(db_name,table_name): #Databesede belirtilen tablo yoksa tabloyu oluşturur.
    conn = sqlite3.connect(''+db_name+'.sqlite')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS "+table_name+" ('domain' TEXT NOT NULL, 'price' REAL NOT NULL, PRIMARY KEY('domain'));")
    conn.close()

def irdDatabase(db_name,domain_list): #Apiden dönen sonuçlara göre database ekleme,güncelleme veya silme yapar.
    conn = sqlite3.connect(''+db_name+'.sqlite')
    cur = conn.cursor()
    for dom in domain_list:
            if "purchasable" in dom:
                cur.execute("INSERT OR REPLACE INTO "+ table_name +" (domain,price) VALUES (?,?)",(dom["domainName"],dom["purchasePrice"]))
                conn.commit()
            #else:
            #    cur.execute("SELECT * FROM "+ table_name + " WHERE domain="+dom["domainName"]+"")
            #    row = cur.fetchone()
            #    if row != None:
            #        cur.execute("DELETE FROM "+ table_name + " WHERE domain="+dom["domainName"]+"")
            #        conn.commit()
    conn.close()

def getAllFilesInFolder(root_path, f_ext): #Python dosyasının olduğu dizindeki ve alt klasörlerindeki tüm ext uzantılı dosyaların yollarını döndürür.
    all_files = []
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if filename.lower().endswith(f_ext):
                all_files.append(os.path.join(root, filename))
    return all_files

def main():
    #root = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #files = getAllFilesInFolder(root, f_ext)
    #for txt in files:
    #    domains = readDomainsFromTXT(txt)
    #    print(domains)
    #    checkDomains(username,token,domains,db_name,table_name)
    for i in range(10):
        domains = createRandomDomainList(5)
        checkDomains(username,token,domains,db_name,table_name)

if __name__ == "__main__":
    main()