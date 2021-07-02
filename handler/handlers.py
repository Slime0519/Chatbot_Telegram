from telegram.ext import MessageHandler, Filters, CommandHandler  # import modules
from handler.handler_modules import *

def addhandlers(dispatcher):
    checknew_handler = CommandHandler('checknew', check_new_notice)
    dispatcher.add_handler(checknew_handler)

    print_handler = CommandHandler('printnotice', print_notice)
    dispatcher.add_handler(print_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    #echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    #dispatcher.add_handler(echo_handler)
    gpt_handler = MessageHandler(Filters.text & (~Filters.command), GPThandler)
    dispatcher.add_handler(gpt_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)