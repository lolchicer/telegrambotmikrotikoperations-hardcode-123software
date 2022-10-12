from email import message
import logging
import os
import errorHandling
import commands
from functions import config
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    botCreds = config.GetBotCredentials()

    updater = Updater(botCreds['token'])

    dispatcher = updater.dispatcher

    dispatcher.add_error_handler(errorHandling.errorHandle)

    dispatcher.add_handler(CommandHandler("start", commands.start))
    dispatcher.add_handler(CommandHandler("myid", commands.myId))
    dispatcher.add_handler(CommandHandler("connect", commands.connect))
    dispatcher.add_handler(CommandHandler("create", commands.create))
    dispatcher.add_handler(CommandHandler("disable", commands.disable))
    dispatcher.add_handler(CommandHandler("enable", commands.enable))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
