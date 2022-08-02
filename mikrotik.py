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
    

def TryCreateNewSecret(accountName, password, mikrotikCredentials):
    try:
        connection = routeros_api.RouterOsApiPool(mikrotikCredentials['IP'], username=mikrotikCredentials['username'], password=mikrotikCredentials['password'], plaintext_login=mikrotikCredentials['RouterOsGrater642'])
        api = connection.get_api()
        secretsApi = api.get_resource('/ppp/secret')
        secretsList = secretsApi.get()
        for secret in secretsList:
            if secret["name"]== accountName:
                return "Exist"
        secretsApi.add(name=accountName, password=password, service="l2tp", profile="l2tp_profile")
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