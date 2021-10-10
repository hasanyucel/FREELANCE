import requests
from bs4 import BeautifulSoup
from rich import print

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
def getLettersFromURL(url):
    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    letter_table = soup.find('table',attrs={'class':'table table-condensed table-responsive'})
    links = letter_table.find_all('a')
    letters = []
    for val in links:
        get_val = val["href"]
        letters.append(get_val)
    return letters

def getWordsFromURL(letter_url):
    response = requests.request("GET", letter_url, headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    word_list = soup.find('ul',attrs={'class':'lemmalist'})
    links = word_list.find_all('a')
    words = []
    for val in links:
        get_link = val["href"]
        words.append(get_link)
    return words

def insertWordsTXT(url):
    letter_url_list = getLettersFromURL(url)
    with open("linkler.txt", "a") as myfile:
        for letter_url in letter_url_list:
            word_url_list = getWordsFromURL(letter_url)
            for word_url in word_url_list:
                myfile.write(word_url+"\n")


insertWordsTXT("https://www.dwds.de/sitemap")