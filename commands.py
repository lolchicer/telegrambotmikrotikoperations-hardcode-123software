import mailFunctions
import configFunctions
import mikrotikFunctions
import errorHandling
from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    #"""Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Hi {user.mention_markdown_v2()}\!')


def myId(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'SO WHAT DO YOU WANT, SEXY? \r\nYour ID is {user.id}')


def create(update: Update, context: CallbackContext) -> None:
    errorHandling.checkPermission(update)
    
    msgWords = errorHandling.createMsgWords(update)

    newAccountEmail = msgWords[1]
    newAccountPassword = configFunctions.GeneratePassword20()
    mikrotikName = mikrotikFunctions.FindMikrotikName(msgWords[2].lower())
    mikrotikCredentials = mikrotikFunctions.GetMikrotikCredentials(mikrotikName)

    mikrotikFunctions.CreateNewSecret(
        newAccountEmail, newAccountPassword, mikrotikName, mikrotikCredentials)

    mailFunctions.SendAccountInfoToClient(
        newAccountEmail, newAccountPassword, mikrotikCredentials['presharedKey'], mikrotikCredentials['IP'])

    update.message.reply_markdown_v2(
        '\!\!\!SUCCESS\!\!\!\r\nAccout is created\. Mail has sended to the Client\.')


def disable(update: Update, context: CallbackContext) -> None:
    if not errorHandling.checkPermission(update):
        return
    
    mikrotikCredentials = errorHandling.checkCredentials(update)
    
    disable = mikrotikFunctions.DisableASecret(mikrotikCredentials)
    
    if disable == 0:
        update.message.reply_markdown_v2('\!\!\!SUCCESS\!\!\!\r\nAccout is disabled\.')
    if disable == 1:
        update.message.reply_markdown_v2('No such account exists on this Mikrotik\.')
    if disable == 2:
        update.message.reply_markdown_v2('Some exception has thrown when bot try to create and check new account\.\r\nNEED TO MAINTENANCE THE BOT')
