import configFunctions
import formattingFunctions
import mailFunctions
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
    
    msgWords = update.message.text.split()

    formattingFunctions.ValidateMsgWords(msgWords, [formattingFunctions.PLAIN, formattingFunctions.EMAIL, formattingFunctions.PLAIN])

    newAccountEmail = msgWords[1]
    newAccountPassword = configFunctions.GeneratePassword20()
    mikrotikName = configFunctions.GetMikrotikName(msgWords[2].lower())
    mikrotikCredentials = configFunctions.GetMikrotikCredentials(mikrotikName)

    mikrotikFunctions.CreateNewSecret(
        newAccountEmail, newAccountPassword, mikrotikName, mikrotikCredentials)

    mailFunctions.SendAccountInfoToClient(
        newAccountEmail, newAccountPassword, mikrotikCredentials['presharedKey'], mikrotikCredentials['IP'])

    update.message.reply_markdown_v2(
        '\!\!\!SUCCESS\!\!\!\r\nAccout is created\. Mail has sended to the Client\.')


def disable(update: Update, context: CallbackContext) -> None:
    errorHandling.checkPermission(update)

    msgWords = update.message.text.split()

    formattingFunctions.ValidateMsgWords(msgWords, [formattingFunctions.PLAIN, formattingFunctions.EMAIL, formattingFunctions.PLAIN])

    newAccountEmail = msgWords[1]
    newAccountPassword = configFunctions.GeneratePassword20()
    mikrotikName = configFunctions.GetMikrotikName(msgWords[2].lower())
    mikrotikCredentials = configFunctions.GetMikrotikCredentials(mikrotikName)

    mikrotikFunctions.DisableASecret(
        newAccountEmail, mikrotikCredentials)

    mailFunctions.SendAccountInfoToClient(
        newAccountEmail, newAccountPassword, mikrotikCredentials['presharedKey'], mikrotikCredentials['IP'])
    
    update.message.reply_markdown_v2('\!\!\!SUCCESS\!\!\!\r\nAccout is disabled\.')
