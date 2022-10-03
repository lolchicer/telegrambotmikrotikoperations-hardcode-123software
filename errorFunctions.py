import configFunctions
import mikrotik
from telegram import Update
from telegram.ext import CallbackContext


def error_handle(update: Update, context: CallbackContext):
    error = context.error
    if type(error) == mikrotik.ExistingException:
        error = mikrotik.ExistingException(error)
        update.message.reply_markdown_v2(error.message)
        return

    update.message.reply_markdown_v2(
        'Some exception has thrown\.\r\nNEED TO MAINTENANCE THE BOT')
    print(error)


def check_permission(update: Update) -> bool:
    user = update.effective_user
    
    autheticatedIDs = configFunctions.GetAutheticatedIDs()
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
