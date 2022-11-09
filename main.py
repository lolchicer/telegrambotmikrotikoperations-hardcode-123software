from email import message
import logging
import os
import errorHandling
import commands
from functions import config
from telegram import Update
from telegram.ext import Application, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    botCreds = config.GetBotCredentials()

    application = Application.builder().token(botCreds['token']).build()

    application.add_error_handler(errorHandling.errorHandle)

    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("myid", commands.myId))
    application.add_handler(CommandHandler("connect", commands.connect))
    application.add_handler(CommandHandler("create", commands.create))
    application.add_handler(CommandHandler("disable", commands.disable))
    application.add_handler(CommandHandler("enable", commands.enable))
    application.add_handler(CommandHandler("changepassword", commands.changePassword))
    application.add_handler(CommandHandler("changepresharedkey", commands.changePresharedKey))

    # Start the Bot
    application.run_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    application.idle()


if __name__ == "__main__":
    main()
