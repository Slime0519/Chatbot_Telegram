import telegram
from telegram.ext import Updater
from handler.handlers import addhandlers

import private_infomation
import logging
#from torch_handler.api_handler import *


tokenclass = private_infomation.API_TOKEN()
MYTOKEN =  tokenclass.GetToken()
#chat_id = '458591856'


if __name__ == "__main__":
    My_TOKEN_class = private_infomation.API_TOKEN()
    MY_TOKEN = My_TOKEN_class.GetToken()

    bot = telegram.Bot(token=MY_TOKEN)
    updater = Updater(token=MYTOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    addhandlers(dispatcher)

    updater.start_polling(timeout=3, clean=True)
    updater.idle()
