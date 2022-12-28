import requests,time,datetime,os
from rich import print

token = "5918179337:AAHCDENU8i0ItXIPw7FKk6l9PS_wukXWeHk"

def welcome_msg(item):
    chat_id = item["message"]["chat"]["id"]
    user_id = item["message"]["from"]["id"]
    user_name = item["message"]["from"].get("username",user_id)
    first_name = item["message"]["new_chat_member"]["first_name"]
    member_user_name = item["message"]["new_chat_member"]["username"]

    message = f"{first_name} ({member_user_name}) Sefine IFS Telegram grubuna hoş geldiniz!"

    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML&disable_web_page_preview=True'.format(token, chat_id, message)
    resp = requests.get(url)

endTime = datetime.datetime.now() + datetime.timedelta(minutes=3)

old_id = 93702884

while endTime > datetime.datetime.now():
    time.sleep(1)
    base_url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
    resp = requests.get(base_url)
    data = resp.json()
    
    for item in data["result"]:
        new_id = item["update_id"]
        if old_id < new_id:
            old_id = int(item["update_id"])
            print(item)
            try:
                if "new_chat_member" in item["message"]:
                    welcome_msg(item)
            except:
                pass