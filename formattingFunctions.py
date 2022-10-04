import re
import mailFunctions
from telegram import Update


class InvalidCreateEmailFormat(Exception):
    message = 'First argument must be the email address\.\r\nExample: /create info@mail\.ru reshetnikova'


def ValidateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        raise InvalidCreateEmailFormat()


class InvalidCreateMsgWordsFormat(Exception):
    message = 'You should send email and mikrotik name\!\r\nExample: /create info@mail\.ru reshetnikova'


PLAIN = 0
MIKROTIK_ALIAS = 1
EMAIL = 2


def createMsgWords(update: Update, formattings: list[int]) -> list[str]:
    msgWords = update.message.text.split()
    if len(msgWords) != len(format):
        raise InvalidCreateMsgWordsFormat()

    for msgWord, formatting in zip(msgWords, formattings):
        if formatting == PLAIN:
            pass
        if formatting == MIKROTIK_ALIAS:
            pass
        if formatting == EMAIL:
            ValidateEmail(msgWord)
