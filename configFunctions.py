import os
import json
import secrets
import string


class NoAuthenticatedIds(Exception):
    message = 'Server doesn\'t have file with authenticated IDs or get some error, sorry\.'


def GetAutheticatedIds():
    authenticatedIds = 'autheticatedIDs.json'
    
    if not os.path.exists(authenticatedIds):
        raise NoAuthenticatedIds()

    with open(authenticatedIds) as f:
        json_data = json.load(f)
        return json_data


def GetBotCredentials():
    botCredentials = 'botCredentials.json'

    with open(botCredentials) as f:
        json_data = json.load(f)
        return json_data


def GeneratePassword20():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))


class NoMikrotikDefaultSettingsException(Exception):
    message = 'Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.'


def GetMikrotikDefaultSettings(mikrotikName):
    with open('Mikrotiks Default Settings/' + mikrotikName + '.json') as f:
        return json.load(f)


class NoMikrotikCredentialsException(Exception):
    message = 'Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.'


def GetMikrotikCredentials(mikrotikName: str) -> str:
    mikrotikPath = 'Mikrotiks Credentials/' + mikrotikName + '.json'

    if not os.path.exists(mikrotikPath):
        raise NoMikrotikCredentialsException()

    with open(mikrotikPath) as f:
        json_data = json.load(f)
        return json_data


class NoMikrotikNameException(Exception):
    message = 'Server doesn\'t recognize this name of Mikrotik\. Try another one'


def HasMikrotikAliases() -> bool:
    return os.path.exists('mikrotiksAliases.json')


def GetMikrotikNameByAliasItem(mikrotikAliasItem) -> str:
    with open('mikrotiksAliases.json') as f:
        mikrotiksAliases = json.load(f)

        for name, alias in zip(mikrotiksAliases.keys(), mikrotiksAliases.values()):
            if mikrotikAliasItem in alias:
                return name
            

def HasMikrotikCredentials(mikrotikName) -> bool:
    return os.path.exists(f'Mikrotiks Credentials/{mikrotikName}.json')


def GetMikrotikName(mikrotikAliasItem) -> str:
    if HasMikrotikAliases():
        return GetMikrotikNameByAliasItem(mikrotikAliasItem)
    if HasMikrotikCredentials(mikrotikAliasItem):
        # тут должно создаваться исключение об отсутствии конфига, но я не знаю, где оно должно обрабатываться
        return mikrotikAliasItem
    raise NoMikrotikNameException()


def HasPresharedKeys() -> bool:
    return os.path.exists('presharedKeys.json')


class NoPresharedKeyException(Exception):
    message = 'Server doesn\'t have file with preshared keys. Email sending has failed.'


def GetPresharedKey(mikrotikName: str) -> str:
    if HasPresharedKeys():
        with open('presharedKeys.json') as f:
            presharedKeys = json.load(f)

            return presharedKeys[mikrotikName]
    raise NoPresharedKeyException()


def GetSmtpCredentials():
    mailCredentials = 'mailCredentials.json'

    with open('mailCredentials.json') as f:
        json_data = json.load(f)
        tmp = json_data['smtp_server']
        tmp = json_data['sender_email']
        tmp = json_data['password']
        return json_data
