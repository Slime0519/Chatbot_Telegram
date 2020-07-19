import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
from time import sleep
import threading, time
import HTML_API_TOKEN
import crawler_function

tokenclass = HTML_API_TOKEN.API_TOKEN()
MYTOKEN =  tokenclass.GetToken()
chat_id = '458591856'


# start
def start(bot,update):
    global chat_id
    chat_id = update.message.chat.id
    update.message.reply_text("Hi. I'm Junmyeong Bot")

# change from people
def check_new_notice(bot, update) :
    crawler_function.print_notice(bot=bot, chat_id=chat_id,newarticlecheck=1)

def print_notice(bot,update):
    crawler_function.print_notice(bot=bot, chat_id=chat_id, newarticlecheck=0)

def help(bot, update):
    helphead ="<command list>\n"
    commandlist = "/start : start chatbot\n" + "/checknew : check new notice\n" + "/printnotice : print recent notice\n"
    update.message.reply_text(helphead + commandlist)

if __name__ == "__main__":
    My_TOKEN_class = HTML_API_TOKEN.API_TOKEN()
    MY_TOKEN = My_TOKEN_class.GetToken()

    bot = telegram.Bot(token=MY_TOKEN)
    updater = Updater(MYTOKEN)

    checknew_handler = CommandHandler('checknew', check_new_notice)
    updater.dispatcher.add_handler(checknew_handler)

    print_handler = CommandHandler('printnotice',print_notice)
    updater.dispatcher.add_handler(print_handler)

    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help',help)
    updater.dispatcher.add_handler(help_handler)

    updater.start_polling(timeout=3, clean=True)
    updater.idle()
