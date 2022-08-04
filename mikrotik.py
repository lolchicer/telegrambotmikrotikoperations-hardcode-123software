import routeros_api
import json

def FindMikrotikName(mikrotikAliasItem):
    mikrotikName = None
    
    with open('mikrotiksAliases.json') as f:
        mikrotiksAliases = json.load(f)
        
        for name, alias in zip(mikrotiksAliases.keys(), mikrotiksAliases.values()):
            if mikrotikAliasItem in alias:
                mikrotikName = name
    
    return mikrotikName


def GetMikrotikDefaultSettings(mikrotikName):
    with open('Mikrotiks Default Settings/' + mikrotikName + '.json') as f:
        return json.load(f)


def TryGetMikrotikCredentials(mikrotikName):
    try:
        with open('Mikrotiks Credentials/' + mikrotikName + '.json') as f:
            json_data = json.load(f)
            tmp = json_data['IP']
            tmp = json_data['username']
            tmp = json_data['password']
            tmp = json_data['presharedKey']
            tmp = json_data['RouterOsGrater642']            
            return json_data
    except (FileNotFoundError, KeyError):
        return False


class ExistingException(Exception):
    message = 'This account already exist on this Mikrotik\.'
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    

def TryCreateNewSecret(accountName, password, mikrotikName, mikrotikCredentials):
    try:
        connection = routeros_api.RouterOsApiPool(mikrotikCredentials['IP'], username=mikrotikCredentials['username'], password=mikrotikCredentials['password'], plaintext_login=mikrotikCredentials['RouterOsGrater642'])
        api = connection.get_api()
        secretsApi = api.get_resource('/ppp/secret')
        secretsList = secretsApi.get()
        for secret in secretsList:
            if secret["name"]== accountName:
                raise ExistingException()
        secretsApi.add(name=accountName, password=password, **GetMikrotikDefaultSettings(mikrotikName))
        connection.disconnect()

        #check creation
        connection = routeros_api.RouterOsApiPool(mikrotikCredentials['IP'], username=mikrotikCredentials['username'], password=mikrotikCredentials['password'], plaintext_login=mikrotikCredentials['RouterOsGrater642'])
        api = connection.get_api()
        secretsApi = api.get_resource('/ppp/secret')
        secretsList = secretsApi.get()
        for secret in secretsList:
            if secret["name"]== accountName:
                connection.disconnect()
                return True
        connection.disconnect()
        return False
    except Exception as e:
        print(e)
        return "Exception"