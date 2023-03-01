from functions import config, formatting, mail, mikrotik, other
import errorHandling
from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    #"""Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(f"Hi {user.mention_markdown_v2()}\!")


def myId(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        f"SO WHAT DO YOU WANT, SEXY? \r\nYour ID is {user.id}")


# нужно отправлять что-то со стороны микротика для наглядности
def connect(update: Update, context: CallbackContext) -> None:
    errorHandling.config.CheckPermission(update.effective_user.id)

    msgWords = update.message.text.split()

    formatting.ValidateMsgWords(msgWords, [formatting.PLAIN, formatting.PLAIN])

    mikrotikName = config.GetMikrotikName(msgWords[1].lower())

    mikrotikCredentials = config.GetMikrotikCredentials(mikrotikName)

    mikrotik.Connect(mikrotikCredentials)


def create(update: Update, context: CallbackContext) -> None:
    errorHandling.config.CheckPermission(update.effective_user.id)

    msgWords = update.message.text.split()

    formatting.ValidateMsgWords(
        msgWords, [formatting.PLAIN, formatting.EMAIL, formatting.PLAIN])

    newAccountEmail = msgWords[1]
    newAccountPassword = other.GeneratePassword20()
    mikrotikName = config.GetMikrotikName(msgWords[2].lower())
    mikrotikCredentials = config.GetMikrotikCredentials(mikrotikName)

    mikrotik.CreateNewSecret(
        newAccountEmail, newAccountPassword, mikrotikName, mikrotikCredentials)

    mail.SendAccountInfoToClient(
        newAccountEmail, newAccountPassword, config.GetPresharedKey(mikrotikName), mikrotikCredentials['host'])

    update.message.reply_markdown_v2(
        "\!\!\!SUCCESS\!\!\!\r\nAccout is created\. Mail has sended to the Client\.")


def disable(update: Update, context: CallbackContext) -> None:
    errorHandling.config.CheckPermission(update.effective_user.id)

    msgWords = update.message.text.split()

    if len(msgWords) == 4:
        formatting.ValidateMsgWords(
            msgWords, [formatting.PLAIN, formatting.EMAIL, formatting.PLAIN, formatting.PLAIN])
    else:
        formatting.ValidateMsgWords(
            msgWords, [formatting.PLAIN, formatting.EMAIL, formatting.PLAIN])

    newAccountEmail = msgWords[1]
    mikrotikName = config.GetMikrotikName(msgWords[2].lower())
    mikrotikCredentials = config.GetMikrotikCredentials(mikrotikName)

    if len(msgWords) == 4:
        reason = msgWords[3]
        mikrotik.DisableASecretWithAReason(
            newAccountEmail, mikrotikCredentials, reason)
    else:
        mikrotik.DisableASecret(
            newAccountEmail, mikrotikCredentials)

    mail.SendDisablingNotificationToClient(
        newAccountEmail, mikrotikCredentials['host'])

    update.message.reply_markdown_v2(
        "\!\!\!SUCCESS\!\!\!\r\nAccout is disabled\. Mail has sended to the Client\.")


def enable(update: Update, context: CallbackContext) -> None:
    errorHandling.config.CheckPermission(update.effective_user.id)

    msgWords = update.message.text.split()

    if len(msgWords) == 4:
        formatting.ValidateMsgWords(
            msgWords, [formatting.PLAIN, formatting.EMAIL, formatting.PLAIN, formatting.PLAIN])
    else:
        formatting.ValidateMsgWords(
            msgWords, [formatting.PLAIN, formatting.EMAIL, formatting.PLAIN])

    accountEmail = msgWords[1]
    newAccountPassword = other.GeneratePassword20()
    mikrotikName = config.GetMikrotikName(msgWords[2].lower())
    mikrotikCredentials = config.GetMikrotikCredentials(mikrotikName)

    if len(msgWords) == 4:
        reason = msgWords[3]
        mikrotik.EnableASecretWithAReason(
            accountEmail, mikrotikCredentials, newAccountPassword, reason)
    else:
        mikrotik.EnableASecret(
            accountEmail, mikrotikCredentials, newAccountPassword)

    mail.SendEnablingNotificationToClient(
        accountEmail, newAccountPassword, mikrotikCredentials['host'])

    update.message.reply_markdown_v2(
        "\!\!\!SUCCESS\!\!\!\r\nAccout is enabled\. Mail has sended to the Client\.")


def changePassword(update: Update, context: CallbackContext) -> None:
    errorHandling.config.CheckPermission(update.effective_user.id)

    msgWords = update.message.text.split()

    formatting.ValidateMsgWords(
        msgWords, [formatting.PLAIN, formatting.EMAIL, formatting.PLAIN])

    accountEmail = msgWords[1]
    newAccountPassword = other.GeneratePassword20()
    mikrotikName = config.GetMikrotikName(msgWords[2].lower())
    mikrotikCredentials = config.GetMikrotikCredentials(mikrotikName)

    mikrotik.SetPassword(accountEmail, mikrotikCredentials, newAccountPassword)

    mail.SendNewPasswordToClient(
        accountEmail, newAccountPassword, mikrotikCredentials['host'])

    update.message.reply_markdown_v2(
        "\!\!\!SUCCESS\!\!\!\r\nPassword is changed\. Mail has sended to the Client\.")


def changePresharedKey(update: Update, context: CallbackContext) -> None:
    errorHandling.config.CheckPermission(update.effective_user.id)

    msgWords = update.message.text.split()

    formatting.ValidateMsgWords(
        msgWords, [formatting.PLAIN, formatting.PLAIN, formatting.PLAIN])

    newPresharedKey = other.GeneratePassword20()
    mikrotikName = config.GetMikrotikName(msgWords[2].lower())
    mikrotikCredentials = config.GetMikrotikCredentials(mikrotikName)
    l2tpClientName = msgWords[1].lower()

    mikrotik.SetPresharedKey(
        mikrotikCredentials, l2tpClientName, newPresharedKey)
    config.SetPresharedKey(mikrotikName, newPresharedKey)

    accountEmails = mikrotik.GetAllClientsEnabledSecretsNames(mikrotikCredentials)

    mail.SendNewPresharedKeyToClients(
        accountEmails, newPresharedKey, mikrotikCredentials['host'])

    update.message.reply_markdown_v2(
        "\!\!\!SUCCESS\!\!\!\r\nPreshared key is changed\. Mail has sended to the Client\.")
