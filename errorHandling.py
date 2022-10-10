import configFunctions
import exceptions
from telegram import Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown


class NoPermission(exceptions.SentException):
    def __init__(self, sentMessage: str = "You don\'t have permissions to do this.", message = "User doesn't have permissions to use the bot.", *args: object) -> None:
        super().__init__(sentMessage, message, *args)


def checkPermission(update: Update) -> None:
    user = update.effective_user
    
    autheticatedIds = configFunctions.GetAutheticatedIds()
    if user.id not in autheticatedIds['IDs']:
        raise NoPermission()


def errorHandle(update: Update, context: CallbackContext):
    error: exceptions.SentException
    error = context.error
    
    try:
        sentMessage = error.sentMessage
    except Exception:
        sentMessage = "Some exception has thrown.\r\nNEED TO MAINTENANCE THE BOT"
    finally:
        update.message.reply_markdown_v2(escape_markdown(sentMessage, version=2))
        print(error)
