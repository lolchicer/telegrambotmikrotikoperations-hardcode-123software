from functions import config
import exceptions
from telegram import Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown


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
