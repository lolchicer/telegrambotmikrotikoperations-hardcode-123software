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


class NoMikrotikNameException(Exception):
    message = 'Server doesn\'t recognize this name of Mikrotik\. Try another one'


class NoMikrotikDefaultSettingsException(Exception):
    message = 'Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.'


def GetMikrotikDefaultSettings(mikrotikName):
    with open('Mikrotiks Default Settings/' + mikrotikName + '.json') as f:
        return json.load(f)


def GetMikrotikCredentials(mikrotikName):
    mikrotikPath = 'Mikrotiks Credentials/' + mikrotikName + '.json'

    if not os.path.exists(mikrotikPath):
        raise NoMikrotikCredentialsException()

    with open(mikrotikPath) as f:
        json_data = json.load(f)
        return json_data


class NoMikrotikCredentialsException(Exception):
    message = 'Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.'


def FindMikrotikName(mikrotikAliasItem):
    mikrotikName = None

    with open('mikrotiksAliases.json') as f:
        mikrotiksAliases = json.load(f)

        for name, alias in zip(mikrotiksAliases.keys(), mikrotiksAliases.values()):
            if mikrotikAliasItem in alias:
                mikrotikName = name

    if mikrotikName == None:
        raise NoMikrotikNameException()

    return mikrotikName
