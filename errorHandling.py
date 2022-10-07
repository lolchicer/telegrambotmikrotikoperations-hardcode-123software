import configFunctions
import exceptions
import mailFunctions
import mikrotikFunctions
from telegram import Update
from telegram.ext import CallbackContext


class NoPermission(Exception):
    message = 'You don\'t have permissions to do this\.'


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
        sentMessage = 'Some exception has thrown\.\r\nNEED TO MAINTENANCE THE BOT'
    finally:
        update.message.reply_markdown_v2(sentMessage)
        print(error)
