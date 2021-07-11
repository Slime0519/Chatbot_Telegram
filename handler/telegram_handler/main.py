import telegram
from telegram.ext import Updater
from handler.telegram_handler.handlers import addhandlers
from handler.telegram_handler import serverhandler
import argparse

import private_infomation
import logging

tokenclass = private_infomation.API_TOKEN()
MYTOKEN =  tokenclass.GetToken()

parser = argparse.ArgumentParser()
parser.add_argument('--api_server', type=str)


if __name__ == "__main__":

    args = parser.parse_args();
    serverhandler.setaddr(server_addr = args.api_server)

    My_TOKEN_class = private_infomation.API_TOKEN()
    MY_TOKEN = My_TOKEN_class.GetToken()

    bot = telegram.Bot(token=MY_TOKEN)
    updater = Updater(token=MYTOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    addhandlers(dispatcher)

    updater.start_polling(timeout=3, clean=True)
    updater.idle()
