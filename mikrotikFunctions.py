from tkinter import EXCEPTION
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


def DisableASecret(accountName, mikrotikCredentials):
    # я не знаю разорвёт ли сборщик мусора соединение
    RETURNED = 0
    NO_SUCH_SECRET = 1
    EXCEPTION = 2

    connection = RouterOSApiPoll(mikrotikCredentials)
    api = connection.get_api()
    secretsApi = api.get_resource('/ppp/secret/set/?name={secretName}')
    secretsList = secretsApi.get()
        
    returning = NO_SUCH_SECRET

    for secret in secretsList:
        if secret['name'] == accountName:
            secretsList.set(secret['id'], name=accountName)
            returning = RETURNED

    connection.disconnect

    return returning
