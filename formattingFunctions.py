import re


class InvalidCreateMsgWordsFormat(Exception):
    message = 'You should send email and mikrotik name\!\r\nExample: /create info@mail\.ru reshetnikova'


class InvalidCreateEmailFormat(Exception):
    message = 'First argument must be the email address\.\r\nExample: /create info@mail\.ru reshetnikova'


PLAIN = 0
EMAIL = 2


def ValidateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        raise InvalidCreateEmailFormat()


def ValidateMsgWords(msgWords: list[str], formattings: list[int]) -> None:
    if len(msgWords) != 3:
        raise InvalidCreateMsgWordsFormat()
    
    for msgWord, formatting in zip(msgWords, formattings):
        if formatting == PLAIN:
            pass
        if formatting == EMAIL:
            ValidateEmail(msgWord)
