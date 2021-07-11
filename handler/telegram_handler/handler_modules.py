import requests
from telegram.ext.callbackcontext import CallbackContext
#tokenclass = HTML_API_TOKEN.API_TOKEN()
#MYTOKEN =  tokenclass.GetToken()
#chat_id = '458591856'
# start
from handler.telegram_handler import serverhandler, crawler_function


def start(update, context : CallbackContext):
    global chat_id
    chat_id = update.message.chat.id
    #update.message.reply_text("Hi. I'm Junmyeong Bot")
    context.bot.send_message("Hi. I'm JunmyeongBot.")

# change from people
def check_new_notice(update, context : CallbackContext) :
    chat_id = update.message.chat.id
    crawler_function.print_notice(bot=context.bot, chat_id=chat_id, newarticlecheck=1)

def print_notice(update, context : CallbackContext):
    chat_id = update.message.chat.id
    crawler_function.print_notice(bot=context.bot, chat_id=chat_id, newarticlecheck=0)

def help(update, context : CallbackContext):
    helphead ="<command list>\n"
    commandlist = "/start : start chatbot\n" + "/checknew : check new notice\n" + "/printnotice : print recent notice\n"
    update.message.reply_text(helphead + commandlist)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def GPThandler(update, context):
    content = update.message.text
    response = requests.put(serverhandler.calladdr, data={"data" : content})
    reply = response.text
    context.bot.send_message(chat_id=update.effective_chat.id, text = reply)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Sorry, I didn't understand that command.")
