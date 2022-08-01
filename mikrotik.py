from tkinter import EXCEPTION
import routeros_api
import json

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


def RouterOSApiPoll(mikrotikCredentials):
    return routeros_api.RouterOsApiPool(mikrotikCredentials['IP'], username=mikrotikCredentials['username'], password=mikrotikCredentials['password'], plaintext_login=mikrotikCredentials['RouterOsGrater642'])


def TryDisableASecret(accountName, mikrotikCredentials):
    # я не знаю разорвёт ли сборщик мусора соединение
    RETURNED = 0
    NO_SUCH_SECRET = 1
    EXCEPTION = 2

    try:
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
    except Exception as e:
        print(e)
        return EXCEPTION
