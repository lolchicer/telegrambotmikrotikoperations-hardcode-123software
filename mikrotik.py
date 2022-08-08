import routeros_api
import json
import os.path


class NoMikrotikNameException(Exception):
    message = 'Server doesn\'t recognize this name of Mikrotik\. Try another one'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


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
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def GetMikrotikDefaultSettings(mikrotikName):
    with open('Mikrotiks Default Settings/' + mikrotikName + '.json') as f:
        return json.load(f)


class NoMikrotikCredentialsException(Exception):
    message = 'Some problem with getting mikrotik credentials\.\r\nMaybe server doesn\'t have file with this credentials\.'
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


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

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoResultException(Exception):
    message = 'Tried to create new account\. Operation has no exceptions.\r\nBut by some reason check new account is not passed\.\r\nNEED TO MANUAL TESTING CREATION AND BOT FUNCTIONALITY'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


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
