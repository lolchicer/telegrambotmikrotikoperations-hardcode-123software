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
    user = update.effective_user

    autheticatedIds = configFunctions.GetAutheticatedIds()
    if user.id not in autheticatedIds['IDs']:
        update.message.reply_markdown_v2(
            'You don\'t have permissions to do this\.')
        return

    msgWords = update.message.text.split()
    if len(msgWords) != 3:
        update.message.reply_markdown_v2(
            'You should send email and mikrotik name\!\r\nExample: /create info@mail\.ru reshetnikova')
        return
    if not mailFunctions.ValidateEmail(msgWords[1]):
        update.message.reply_markdown_v2(
            'First argument must be the email address\.\r\nExample: /create info@mail\.ru reshetnikova')
        return

    clientEmail = msgWords[1]

    mikrotikName = mikrotikFunctions.FindMikrotikName(msgWords[2].lower())

    mikrotikCredentials = mikrotikFunctions.GetMikrotikCredentials(mikrotikName)

    newAccountPassword = configFunctions.GeneratePassword20()

    return mikrotikCredentials

    mikrotikFunctions.CreateNewSecret(
        clientEmail, newAccountPassword, mikrotikName, mikrotikCredentials)

    mailFunctions.SendAccountInfoToClient(
        clientEmail, newAccountPassword, mikrotikCredentials['presharedKey'], mikrotikCredentials['IP'])

    update.message.reply_markdown_v2(
        '\!\!\!SUCCESS\!\!\!\r\nAccout is created\. Mail has sended to the Client\.')


def disable(update: Update, context: CallbackContext) -> None:
    if not errorHandling.checkPermission(update):
        return
    
    mikrotikCredentials = errorHandling.checkCredentials(update)
    
    disable = mikrotikFunctions.TryDisableASecret(mikrotikCredentials)
    
    if disable == 0:
        update.message.reply_markdown_v2('\!\!\!SUCCESS\!\!\!\r\nAccout is disabled\.')
    if disable == 1:
        update.message.reply_markdown_v2('No such account exists on this Mikrotik\.')
    if disable == 2:
        update.message.reply_markdown_v2('Some exception has thrown when bot try to create and check new account\.\r\nNEED TO MAINTENANCE THE BOT')
