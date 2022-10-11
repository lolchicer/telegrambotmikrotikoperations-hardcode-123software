import json
import secrets
import string
import exceptions
import configPaths


class NoConfigError(exceptions.SentException):
    def __init__(self, path: str) -> None:
        super().__init__(f"Missing file \"{path}\".")


class InvalidConfigError(exceptions.SentException):
    def __init__(self, path: str) -> None:
        super().__init__(f"Config file \"{path}\" has invalid format.")


def GetConfig(path: str):
    try:
        with open(path) as f:
            json_data = json.load(f)
        return json_data
    except FileNotFoundError:
        raise NoConfigError(path)
    except ValueError:
        raise InvalidConfigError(path)


def GetBotCredentials():
    return GetConfig(configPaths.botCredentials)


def GetAutheticatedIds():
    return GetConfig(configPaths.authenticatedIds)


def GetMailCredentials():
    return GetConfig(configPaths.mailCredentials)


class NoMikrotikAliasError(Exception):
    def __init__(self, path: str) -> None:
        super().__init__(
            f"\"{path}\" doesn't have name of Mikrotik for this alias member.")


def GetMikrotikAlias(mikrotikAliasItem) -> str:
    try:
        mikrotiksAliases = GetConfig(configPaths.mikrotiksAliases)
        for name, alias in zip(mikrotiksAliases.keys(), mikrotiksAliases.values()):
            if mikrotikAliasItem in alias:
                return name
    # классы sendexception не желательно указывать в except, т.к. они предназначены для обработки только внутри errorhandler
    # их следует заменить на что-либо ещё, в чём нет полей, содержимое которых будет отправляться пользователю
    # это делается для разделения исключений, отображающих критические ошибки, и исключений, отображающих неправильный ввод и т.д.
    except exceptions.SentException as error:
        print(error.sentMessage)

    raise NoMikrotikAliasError(configPaths.mikrotiksAliases)


def GetMikrotikName(mikrotikAliasItem) -> str:
    try:
        return GetMikrotikAlias(mikrotikAliasItem)
    except NoMikrotikAliasError:
        return mikrotikAliasItem


def GetMikrotikCredentials(mikrotikName: str):
    return GetConfig(configPaths.MikrotikCredentials(mikrotikName))


def GetMikrotikDefaultSettings(mikrotikName: str):
    return GetConfig(configPaths.MikrotikDefaultSettings(mikrotikName))


class NoPresharedKeyError(exceptions.SentException):
    def __init__(self) -> None:
        super().__init__("Server doesn\'t have preshared key for this Mikrotik. Email sending has failed.")


def GetPresharedKey(mikrotikName: str) -> str:
    presharedKeys = GetConfig(configPaths.presharedKeys)

    try:
        return presharedKeys[mikrotikName]
    except KeyError:
        raise NoPresharedKeyError()


def GeneratePassword20():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))
