from functions import config
import exceptions
from telegram import Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown


class NoPermission(exceptions.SentException):
    def __init__(self) -> None:
        super().__init__("You don\'t have permissions to do this.")


def checkPermission(update: Update) -> None:
    user = update.effective_user
    
    autheticatedIds = configFunctions.GetAutheticatedIds()
    if user.id not in autheticatedIds['IDs']:
        raise NoPermission()


def errorHandle(update: Update, context: CallbackContext):
    error = context.error
    
    if exceptions.SentException in error.__class__.__bases__:
        annotatedError: exceptions.SentException
        annotatedError = error
        sentMessage = annotatedError.sentMessage
    else:
        print(error)

        sentMessage = "Some exception has thrown.\r\nNEED TO MAINTENANCE THE BOT"
    
    update.message.reply_markdown_v2(escape_markdown(sentMessage, version=2))
