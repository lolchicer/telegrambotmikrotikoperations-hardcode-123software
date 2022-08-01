from email import message
import logging
import mikrotik
import secrets
import string
import json
import mailFunctions
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():

    botCreds = TryGetBotCredentials()
    if botCreds == False:
        return

    updater = Updater(botCreds['token'])

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("myid", myID))
    dispatcher.add_handler(CommandHandler("create", create))

    dispatcher.add_handler(CommandHandler("suspend", disable))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def start(update: Update, context: CallbackContext) -> None:
    #"""Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Hi {user.mention_markdown_v2()}\!')

def myID(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(f'SO WHAT DO YOU WANT, SEXY? \r\nYour ID is {user.id}')

def create(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    autheticatedIDs = TryGetAutheticatedIDs()
    if autheticatedIDs == False:
        update.message.reply_markdown_v2('Server doesn\'t have file with authenticated IDs or get some error, sorry.')
        return
    if user.id not in autheticatedIDs['IDs']:
        update.message.reply_markdown_v2('You don\'t have permissions to do this\.')        
        return

    msgWords = update.message.text.split()
    if len(msgWords) != 3  :
        update.message.reply_markdown_v2('You should send email and mikrotik name\!\r\nExample: /create info@mail\.ru reshetnikova')
        return
    if not mailFunctions.ValidateEmail(msgWords[1]):
        update.message.reply_markdown_v2('First argument must be the email address\.\r\nExample: /create info@mail\.ru reshetnikova')
        return

    clientEmail = msgWords[1]
    
    RESHETNIKOVA_ALIAS = ['reshetnikova', 'resh', 'r']
    LITEYNII_ALIAS = ['liteynii', 'liteinii', 'litei', 'l', 'litey', 'lit']
    HOME_ALIAS = ['home', 'h']

    for item in [
        tuple('Reshetnikova', RESHETNIKOVA_ALIAS),
        tuple('Liteynii', LITEYNII_ALIAS),
        tuple('Home', HOME_ALIAS)
    ]:
        if msgWords[2].lower() in item[2]:
            mikrotikName = item[1]
    
    if mikrotikName == None:
        update.message.reply_markdown_v2('Server doesn\'t recognize this name of Mikrotik\. Try another one')
        return
            

    mikrotikCredentials = mikrotik.TryGetMikrotikCredentials(mikrotikName)
    if mikrotikCredentials == False:
        update.message.reply_markdown_v2('Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.')
        return

    newAccountPassword = GeneratePassword20()

    created = mikrotik.TryCreateNewSecret(clientEmail, newAccountPassword, mikrotikCredentials)
    if created == 'Exist':
        update.message.reply_markdown_v2('This account already exist on this Mikrotik\.')
        return
    if created == False:
        update.message.reply_markdown_v2('Tried to create new account\. Operation has no exceptions.\r\nBut by some reason check new account is not passed\.\r\nNEED TO MANUAL TESTING CREATION AND BOT FUNCTIONALITY')
        return
    if created == 'Exception':
        update.message.reply_markdown_v2('Some exception has thrown when bot try to create and check new account\.\r\nNEED TO MAINTENANCE THE BOT')
        return
    
    sended = mailFunctions.TrySendAccountInfoToClient(clientEmail, newAccountPassword, mikrotikCredentials['presharedKey'], mikrotikCredentials['IP'])
    if sended == False:
        update.message.reply_markdown_v2('Account is created\.\r\nBUT\! Some problem was caused with sending email to client\.\r\nNEED TO SEND CREDS MANUALY')
        return
    
        
    update.message.reply_markdown_v2('\!\!\!SUCCESS\!\!\!\r\nAccout is created\. Mail has sended to the Client\.')


def check_permission(update: Update) -> bool:
    user = update.effective_user
    
    autheticatedIDs = TryGetAutheticatedIDs()
    if autheticatedIDs == False:
        update.message.reply_markdown_v2('Server doesn\'t have file with authenticated IDs or get some error, sorry.')
        return False
    if user.id not in autheticatedIDs['IDs']:
        update.message.reply_markdown_v2('You don\'t have permissions to do this\.')        
        return False
    
    return True


def check_name(update: Update) -> bool:
    RESHETNIKOVA_ALIAS = ['reshetnikova', 'resh', 'r']
    LITEYNII_ALIAS = ['liteynii', 'liteinii', 'litei', 'l', 'litey', 'lit']
    HOME_ALIAS = ['home', 'h']

    msgWords = update.message.text.split()
    
    for item in [
        tuple('Reshetnikova', RESHETNIKOVA_ALIAS),
        tuple('Liteynii', LITEYNII_ALIAS),
        tuple('Home', HOME_ALIAS)
    ]:
        if msgWords[1].lower() in item[2]:
            mikrotikName = item[1]
    
    if mikrotikName == None:
        update.message.reply_markdown_v2('Server doesn\'t recognize this name of Mikrotik\. Try another one')
    
    return mikrotikName


def check_credentials(update: Update) -> bool:
    mikrotikName = check_name(update)

    if mikrotikName == None:
        return
    
    mikrotikCredentials = mikrotik.TryGetMikrotikCredentials(mikrotikName)
    if mikrotikCredentials == False:
        update.message.reply_markdown_v2('Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.')
    
    return mikrotikCredentials


def disable(update: Update, context: CallbackContext) -> None:
    if not check_permission(update):
        return
    
    mikrotikCredentials = check_credentials(update)
    
    disable = mikrotik.TryDisableASecret(mikrotikCredentials)
    
    if disable == 0:
        update.message.reply_markdown_v2('\!\!\!SUCCESS\!\!\!\r\nAccout is disabled\.')
    if disable == 1:
        update.message.reply_markdown_v2('No such account exists on this Mikrotik\.')
    if disable == 2:
        update.message.reply_markdown_v2('Some exception has thrown when bot try to create and check new account\.\r\nNEED TO MAINTENANCE THE BOT')
    

def TryGetAutheticatedIDs():
    try:
        with open('autheticatedIDs.json') as f:
            json_data = json.load(f)
            tmp = json_data['IDs']
            return json_data
    except (FileNotFoundError, KeyError):
        return False

def TryGetBotCredentials():
    try:
        with open('botCredentials.json') as f:
            json_data = json.load(f)
            tmp = json_data['token']
            return json_data
    except (FileNotFoundError, KeyError):
        return False

def GeneratePassword20():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))   

if __name__ == "__main__":
    main()