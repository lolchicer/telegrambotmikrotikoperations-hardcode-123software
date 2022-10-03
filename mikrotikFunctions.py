from tkinter import EXCEPTION
from typing import Any
import routeros_api
import json
import os.path


class NoMikrotikNameException(Exception):
    message = 'Server doesn\'t recognize this name of Mikrotik\. Try another one'


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


class NoMikrotikDefaultSettingsException(Exception):
    message = 'Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.'


def GetMikrotikDefaultSettings(mikrotikName):
    with open('Mikrotiks Default Settings/' + mikrotikName + '.json') as f:
        return json.load(f)


class NoMikrotikCredentialsException(Exception):
    message = 'Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.'


def GetMikrotikCredentials(mikrotikName):
    mikrotikPath = 'Mikrotiks Credentials/' + mikrotikName + '.json'

    if not os.path.exists(mikrotikPath):
        raise NoMikrotikCredentialsException()

    with open(mikrotikPath) as f:
        json_data = json.load(f)
        tmp = json_data['IP']
        tmp = json_data['username']
        tmp = json_data['password']
        tmp = json_data['presharedKey']
        tmp = json_data['RouterOsGrater642']
        return json_data


class ExistingException(Exception):
    message = 'This account already exist on this Mikrotik\.'


class NoResultException(Exception):
    message = 'Tried to create new account\. Operation has no exceptions.\r\nBut by some reason check new account is not passed\.\r\nNEED TO MANUAL TESTING CREATION AND BOT FUNCTIONALITY'


class CreateAccountException(Exception):
    message = 'Some exception has thrown when bot try to create and check new account\.\r\nNEED TO MAINTENANCE THE BOT'


def CreateNewSecret(accountName, password, mikrotikName, mikrotikCredentials):
    connection = routeros_api.RouterOsApiPool(mikrotikCredentials['IP'], username=mikrotikCredentials['username'],
                                              password=mikrotikCredentials['password'], plaintext_login=mikrotikCredentials['RouterOsGrater642'])
    api = connection.get_api()
    secretsApi = api.get_resource('/ppp/secret')
    secretsList = secretsApi.get()
    for secret in secretsList:
        if secret["name"] == accountName:
            raise ExistingException()
    secretsApi.add(name=accountName, password=password, **
                   GetMikrotikDefaultSettings(mikrotikName))
    connection.disconnect()

    # check creation
    connection = routeros_api.RouterOsApiPool(mikrotikCredentials['IP'], username=mikrotikCredentials['username'],
                                              password=mikrotikCredentials['password'], plaintext_login=mikrotikCredentials['RouterOsGrater642'])
    api = connection.get_api()
    secretsApi = api.get_resource('/ppp/secret')
    secretsList = secretsApi.get()
    for secret in secretsList:
        if secret["name"] == accountName:
            connection.disconnect()
            return
    connection.disconnect()
    raise NoResultException(Exception)


def RouterOSApiPoll(mikrotikCredentials):
    return routeros_api.RouterOsApiPool(mikrotikCredentials['IP'], username=mikrotikCredentials['username'], password=mikrotikCredentials['password'], plaintext_login=mikrotikCredentials['RouterOsGrater642'])


class NoAccountException(Exception):
    message = 'No such account exists on this Mikrotik\.'


class EditAccountException(Exception):
    message = 'Some exception has thrown when bot try edit the account\.\r\nNEED TO MAINTENANCE THE BOT'


def EditSecret(mikrotikCredentials, name: str, properties: dict) -> None:
    RETURNED = 0
    NO_SUCH_SECRET = 1
    ANY = 2

    state = NO_SUCH_SECRET

    try:
        connection = RouterOSApiPoll(mikrotikCredentials)
        api = connection.get_api()
        secretsApi = api.get_resource('/ppp/secret/set/?name={secretName}')
        secretsList = secretsApi.get()

        for secret in secretsList:
            if secret['name'] == name:
                secretsList.set(id=secret['id'], **properties)
                
                state = RETURNED 
        
                break
    except Exception:
        raise EditAccountException()
    finally:
        # я не знаю разорвёт ли сборщик мусора соединение
        connection.disconnect()

        if state == NO_SUCH_SECRET:
            raise NoAccountException()


def DisableASecret(name, mikrotikCredentials) -> None:
    EditSecret(mikrotikCredentials, name, {'disabled': 'yes'})
