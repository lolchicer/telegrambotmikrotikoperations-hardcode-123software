import os
import json
import secrets
import string


class NoAuthenticatedIDs(Exception):
    message = 'Server doesn\'t have file with authenticated IDs or get some error, sorry.'

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def GetAutheticatedIDs():
    authenticatedIDs = 'autheticatedIDs.json'
    
    if not os.path.exists(authenticatedIDs):
        raise NoAuthenticatedIDs()

    with open(authenticatedIDs) as f:
        json_data = json.load(f)
        tmp = json_data['IDs']
        return json_data


def GetBotCredentials():
    botCredentials = 'botCredentials.json'

    with open(botCredentials) as f:
        json_data = json.load(f)
        tmp = json_data['token']
        return json_data


def GeneratePassword20():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))
