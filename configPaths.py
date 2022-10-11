botCredentials = "botCredentials.json"
authenticatedIds = "autheticatedIDs.json"
mikrotiksAliases = "mikrotiksAliases.json"
presharedKeys = "presharedKeys.json"
mailCredentials = "mailCredentials.json"


MikrotiksCredentials = "Mikrotiks Credentails"
MikrotiksDefaultSettings = "Mikrotiks Default Settings"


def MikrotikCredentials(mikrotikName) -> str:
    return f"{MikrotiksCredentials}/{mikrotikName}.json"


def MikrotikDefaultSettings(mikrotikName) -> str:
    return f"{MikrotiksDefaultSettings}/{mikrotikName}.json"


def ConfigTemplates(configName) -> str:
    return f"Config Templates/{configName}.json"
