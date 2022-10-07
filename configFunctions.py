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
    pass


def GetMikrotikAlias(mikrotikAliasItem) -> str:
    mikrotiksAliases = GetConfig(configPaths.mikrotiksAliases)

    for name, alias in zip(mikrotiksAliases.keys(), mikrotiksAliases.values()):
        if mikrotikAliasItem in alias:
            return name
    raise NoMikrotikAliasError(f"\"{configPaths.mikrotiksAliases}\" doesn't have name of Mikrotik for this alias member.")


class NoMikrotikNameError(exceptions.SentException):
    def __init__(self, sentMessage: str = "Server doesn't recognize this name of Mikrotik. Try another one", *args: object) -> None:
        super().__init__(sentMessage, *args)


def GetMikrotikName(mikrotikAliasItem) -> str:
    try:
        return GetMikrotikAlias(mikrotikAliasItem)
    except (NoMikrotikAliasError, NoConfigError) as error:
        print(error)
        return mikrotikAliasItem


class NoPresharedKeyError(exceptions.SentException):
    def __init__(self, sentMessage: str = "Server doesn\'t have file with preshared keys. Email sending has failed.", *args: object) -> None:
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
