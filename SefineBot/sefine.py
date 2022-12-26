import requests,time,datetime,os

token = os.getenv("TELEGRAM_TOKEN")

def welcome_msg(item,keywords):
    chat_id = item["message"]["chat"]["id"]
    user_id = item["message"]["from"]["id"]
    user_name = item["message"]["from"].get("username",user_id)

    message = f"{username} Sefine IFS Telegram grubuna hoş geldiniz!"

    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML&disable_web_page_preview=True'.format(token, chat_id, message)
    resp = requests.get(url)

endTime = datetime.datetime.now() + datetime.timedelta(minutes=3)

old_id = 0

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