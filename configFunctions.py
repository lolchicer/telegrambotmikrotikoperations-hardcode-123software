import json
import secrets
import string
import exceptions
import configPaths


class NoConfigError(exceptions.SentException):
    def __init__(self, path: str, *args: object) -> None:
        sentMessage = f"Missing file \"{path}\"."
        super().__init__(sentMessage, *args)


class InvalidConfigError(exceptions.SentException):
    def __init__(self, path: str, *args: object) -> None:
        sentMessage = f"Config file \"{path}\" has invalid format."
        super().__init__(sentMessage, *args)


def GetConfig(path: str):
    try:
        with open(path) as f:
            json_data = json.load(f)
        return json_data
    except FileNotFoundError as error:
        raise NoConfigError(path, error)
    except ValueError as error:
        raise InvalidConfigError(path, error)


def GetBotCredentials():
    return GetConfig(configPaths.botCredentials)


def GetAutheticatedIds():
    return GetConfig(configPaths.authenticatedIds)


def GetMailCredentials():
    return GetConfig(configPaths.mailCredentials)


class NoMikrotikAliasError(Exception):
    def __init__(self, path: str, *args: object) -> None:
        super().__init__(f"\"{path}\" doesn't have name of Mikrotik for this alias member.")


def GetMikrotikAlias(mikrotikAliasItem) -> str:
    mikrotiksAliases = GetConfig(configPaths.mikrotiksAliases)

    for name, alias in zip(mikrotiksAliases.keys(), mikrotiksAliases.values()):
        if mikrotikAliasItem in alias:
            return name
    raise NoMikrotikAliasError(configPaths.mikrotiksAliases)


class NoMikrotikNameError(exceptions.SentException):
    def __init__(self, sentMessage: str = "Server doesn't recognize this name of Mikrotik. Try another one", *args: object) -> None:
        super().__init__(sentMessage, *args)


# классы sendexception не желательно указывать в except, т.к. они предназначены для обработки только внутри errorhandler
# их следует заменить на что-либо ещё, в чём нет полей, содержимое которых будет отправляться пользователю
# это делается для разделения исключений, отображающих критические ошибки, и исключений, отображающих неправильный ввод и т.д.
def GetMikrotikName(mikrotikAliasItem) -> str:
    try:
        return GetMikrotikAlias(mikrotikAliasItem)
    except (NoMikrotikAliasError, NoConfigError, InvalidConfigError) as error:
        print(error)
        return mikrotikAliasItem


class NoPresharedKeyError(exceptions.SentException):
    def __init__(self, sentMessage: str = "Server doesn\'t have preshared key for this Mikrotik. Email sending has failed.", *args: object) -> None:
        super().__init__(sentMessage, *args)


def GetMikrotikCredentials(mikrotikName: str):
    return GetConfig(configPaths.MikrotikCredentials(mikrotikName))


def GetMikrotikDefaultSettings(mikrotikName: str):
    return GetConfig(configPaths.MikrotikDefaultSettings(mikrotikName))

    
def GetPresharedKey(mikrotikName: str) -> str:
    presharedKeys = GetConfig(configPaths.presharedKeys)
    
    try:
        return presharedKeys[mikrotikName]
    except KeyError as error:
        raise NoPresharedKeyError(error)


def GeneratePassword20():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))
