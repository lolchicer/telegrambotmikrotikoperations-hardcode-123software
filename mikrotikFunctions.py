import routeros_api
import exceptions
import configFunctions


def Connect(mikrotikCredentails):
    connection = routeros_api.RouterOsApiPool(**mikrotikCredentails)
    connection.get_api()
    connection.disconnect()


class ExistingException(exceptions.SentException):
    def __init__(self, sentMessage: str = 'This account already exist on this Mikrotik\.', *args: object) -> None:
        super().__init__(sentMessage, *args)


class NoResultException(exceptions.SentException):
    def __init__(self, sentMessage: str = 'Tried to create new account\. Operation has no exceptions.\r\nBut by some reason check new account is not passed\.\r\nNEED TO MANUAL TESTING CREATION AND BOT FUNCTIONALITY', *args: object) -> None:
        super().__init__(sentMessage, *args)


class CreateAccountException(exceptions.SentException):
    def __init__(self, sentMessage: str = 'Some exception has thrown when bot try to create and check new account\.\r\nNEED TO MAINTENANCE THE BOT', *args: object) -> None:
        super().__init__(sentMessage, *args)


def CreateNewSecret(accountName, password, mikrotikName, mikrotikCredentials):
    try:
        connection = routeros_api.RouterOsApiPool(**mikrotikCredentials)
        api = connection.get_api()
        secretsApi = api.get_resource('/ppp/secret')
        secretsList = secretsApi.get()
        for secret in secretsList:
            if secret["name"] == accountName:
                raise ExistingException()
        secretsApi.add(name=accountName, password=password, **
                    configFunctions.GetMikrotikDefaultSettings(mikrotikName))
        connection.disconnect()

        # check creation
        connection = routeros_api.RouterOsApiPool(**mikrotikCredentials)
        api = connection.get_api()
        secretsApi = api.get_resource('/ppp/secret')
        secretsList = secretsApi.get()
        for secret in secretsList:
            if secret["name"] == accountName:
                connection.disconnect()
                return
        connection.disconnect()
        raise NoResultException()
    except Exception as error:
        raise CreateAccountException(args=error)


class NoAccountException(exceptions.SentException):
    def __init__(self, sentMessage: str = 'No such account exists on this Mikrotik\.', *args: object) -> None:
        super().__init__(sentMessage, *args)


class EditAccountException(exceptions.SentException):
    def __init__(self, sentMessage: str = 'Some exception has thrown when bot try edit the account\.\r\nNEED TO MAINTENANCE THE BOT', *args: object) -> None:
        super().__init__(sentMessage, *args)


def EditSecret(mikrotikCredentials, name: str, properties: dict) -> None:
    RETURNED = 0
    NO_SUCH_SECRET = 1
    ANY = 2

    state = NO_SUCH_SECRET

    try:
        connection = routeros_api.RouterOsApiPool(**mikrotikCredentials)
        api = connection.get_api()
        secretsApi = api.get_resource(f'/ppp/secret')
        secretsList = secretsApi.get()

        for secret in secretsList:
            if secret['name'] == name:
                secretsApi.set(id=secret['id'], **properties)

                state = RETURNED

                break
    except Exception as error:
        raise EditAccountException(args=error)
    finally:
        # я не знаю разорвёт ли сборщик мусора соединение
        connection.disconnect()

        if state == NO_SUCH_SECRET:
            raise NoAccountException()


def DisableASecret(name, mikrotikCredentials) -> None:
    EditSecret(mikrotikCredentials, name, {'disabled': 'yes'})
    # возмжоно нужна смена открытого ключа для ppp и рассылка нового всем пользователям ppp по почте


def EnableASecret(name, mikrotikCredentials, password) -> None:
    EditSecret(mikrotikCredentials, name, {
               'disabled': 'no', 'password': password})
