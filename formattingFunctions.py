import re
import exceptions


class InvalidCreateMsgWordsFormat(exceptions.SentException):
    def __init__(self, sentMessage: str = "You should send email and mikrotik name!\r\nExample: /create info@mail.ru reshetnikova", *args: object) -> None:
        super().__init__(sentMessage, *args)


class InvalidCreateEmailFormat(exceptions.SentException):
    def __init__(self, sentMessage: str = "First argument must be the email address.\r\nExample: /create info@mail.ru reshetnikova", *args: object) -> None:
        super().__init__(sentMessage, *args)


PLAIN = 0
EMAIL = 2


def ValidateEmail(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if not re.fullmatch(regex, email):
        raise InvalidCreateEmailFormat()


def ValidateMsgWords(msgWords: list[str], formattings: list[int]) -> None:
    if len(msgWords) != len(formattings):
        raise InvalidCreateMsgWordsFormat()
    
    for msgWord, formatting in zip(msgWords, formattings):
        if formatting == PLAIN:
            pass
        if formatting == EMAIL:
            ValidateEmail(msgWord)
