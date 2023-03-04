import requests

url = 'https://bilgibankasi.ito.org.tr/tr/api/job-group-search'

headers = {
    'Content-Type': 'application/json'
}


response = requests.post(url, headers=headers)

print(response.text)
