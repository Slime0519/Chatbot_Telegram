import telegram
from telegram.ext import Updater
from torch_handler.api_handler import addhandlers

import HTML_API_TOKEN
from torch_handler.api_handler import *


tokenclass = HTML_API_TOKEN.API_TOKEN()
MYTOKEN =  tokenclass.GetToken()
#chat_id = '458591856'


if __name__ == "__main__":
    My_TOKEN_class = HTML_API_TOKEN.API_TOKEN()
    MY_TOKEN = My_TOKEN_class.GetToken()

    bot = telegram.Bot(token=MY_TOKEN)
    updater = Updater(token=MYTOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    addhandlers(dispatcher)

    updater.start_polling(timeout=3, clean=True)
    updater.idle()
