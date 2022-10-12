import re
import exceptions


PLAIN = 0
EMAIL = 2


class InvalidCreateEmailFormat(exceptions.SentException):
    def __init__(self) -> None:
        super().__init__("First argument must be the email address.\r\nExample: /create info@mail.ru reshetnikova")


def ValidateEmail(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if not re.fullmatch(regex, email):
        raise InvalidCreateEmailFormat()


class InvalidCreateMsgWordsFormat(exceptions.SentException):
    def __init__(self) -> None:
        super().__init__("You should send email and mikrotik name!\r\nExample: /create info@mail.ru reshetnikova")


def ValidateMsgWords(msgWords: list[str], formattings: list[int]) -> None:
    if len(msgWords) != len(formattings):
        raise InvalidCreateMsgWordsFormat()

    for msgWord, formatting in zip(msgWords, formattings):
        if formatting == PLAIN:
            pass
        if formatting == EMAIL:
            ValidateEmail(msgWord)
