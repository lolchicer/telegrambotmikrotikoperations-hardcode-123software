botCredentials = "botCredentials.json"
authenticatedIds = "autheticatedIDs.json"
mikrotiksAliases = "mikrotiksAliases.json"
presharedKeys = "presharedKeys.json"
mailCredentials = "mailCredentials.json"


def MikrotikCredentials(mikrotikName) -> str:
    return f"Mikrotiks Credentials/{mikrotikName}.json"


def MikrotikDefaultSettings(mikrotikName) -> str:
    return f"Mikrotiks Default Settings/{mikrotikName}.json"
