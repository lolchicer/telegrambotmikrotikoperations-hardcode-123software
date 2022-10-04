import configFunctions
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


def checkName(update: Update) -> bool:
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


def checkCredentials(update: Update) -> bool:
    mikrotikName = checkName(update)

    if mikrotikName == None:
        return
    
    mikrotikCredentials = mikrotikFunctions.TryGetMikrotikCredentials(mikrotikName)
    if mikrotikCredentials == False:
        update.message.reply_markdown_v2('Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.')
    
    return mikrotikCredentials


def errorHandle(update: Update, context: CallbackContext):
    error = context.error
    
    try:
        update.message.reply_markdown_v2(error.message)
    except Exception:
        update.message.reply_markdown_v2('Some exception has thrown\.\r\nNEED TO MAINTENANCE THE BOT')
    finally:
        print(error)
