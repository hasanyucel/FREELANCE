import telegram.ext,json,os
from rich import print

token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

updater = telegram.ext.Updater(token,use_context = True)
dispatcher = updater.dispatcher

def selam(update,context):
    user = update.message.from_user
    adi = user["first_name"]
    dispatcher.bot.sendMessage(chat_id,f"<b>Sefine'ye hoşgeldin {adi}</b>",parse_mode=telegram.ParseMode.HTML)

def help(update,context):
    dispatcher.bot.sendMessage(chat_id,
    """
    <b>Kullanılabilecek komut listesi:</b>\n\n/selam\t\t\t\t\t\tHoşgeldin mesajı.\n/portal\t\t\t\t\t\tSefine Portal linki
    """,parse_mode=telegram.ParseMode.HTML
    )

def portal(update,context):
    update.message.reply_text("https://portal.sefine.com.tr/")

def toplam(update,context):
    i = 1
    j = 2
    update.message.reply_text(i+j)

dispatcher.add_handler(telegram.ext.CommandHandler('selam', selam))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
dispatcher.add_handler(telegram.ext.CommandHandler('portal', portal))
dispatcher.add_handler(telegram.ext.CommandHandler('toplam', toplam))

updater.start_polling()
updater.idle()