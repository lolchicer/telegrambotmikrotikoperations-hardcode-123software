import sys
import json
import smtplib
import ssl
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class CannotSendAccountInfoToClientException(Exception):
    message = 'Account is created\.\r\nBUT\! Some problem was caused with sending email to client\.\r\nNEED TO SEND CREDS MANUALY'

def SendAccountInfoToClient(accountName, accountPassword, presharedKey, IP):
    body = """Добрый день!

Для вас была создана учетная запись для подключения к VPN по адресу IPadd :

Логин: login
Пароль: password

Настройка нового подключения или сети
Подключение к рабочему месту
Создать новое подключение
Использовать мое подключение к интернету (VPN)
Интернет-адрес: IPadd

Вкладка Безопасность:
Тип VPN: L2TP IPSec VPN
Дополнительные параметры: для проверки подлинности использовать предварительный ключ. В нашем случае это: preshared (IP - IPSec - Peers)

Здесь же, в группе "Проверка подлинности", оставляем только CHAP v2"""

    body = body.replace('login', accountName)
    body = body.replace('password', accountPassword)
    body = body.replace('preshared', presharedKey)
    body = body.replace('IPadd', IP)
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendNewPasswordToClent(accountName, accountPassword, IP):
    body = """Добрый день!
    
    Пароль вашей учётной записи login для подключения к VPN по адресу IPadd был изменён:
    
    password"""

    body = body.replace('login', accountName)
    body = body.replace('password', accountPassword)
    body = body.replace('IPadd', IP)
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendDisablingNotificationToClent(accountName, IP):
    body = """Добрый день!
    
    Действие вашей учётной записи login для подключения к VPN по адресу IPadd было приостановлено."""

    body = body.replace('login', accountName)
    body = body.replace('IPadd', IP)
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendEnablingNotificationToClent(accountName, accountPassword, presharedKey, IP):
    body = """Добрый день!
    
    Действие вашей учётной записи login для подключения к VPN по адресу IPadd было восстановлено:
    
    Новый пароль: password
    Новый предварительный ключ: preshared"""

    body = body.replace('login', accountName)
    body = body.replace('password', accountPassword)
    body = body.replace('preshared', presharedKey)
    body = body.replace('IPadd', IP)
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendNewPasswordToClent(accountName, accountPassword, IP):
    body = """Добрый день!
    
    Пароль вашей учётной записи login для подключения к VPN по адресу IPadd был изменён:
    
    password"""

    body = body.replace('login', accountName)
    body = body.replace('password', accountPassword)
    body = body.replace('IPadd', IP)
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendEmailToClient(receiverEmail, subject, body):
    smtpCreds = GetSmtpCredentials()

    port = 465  # For SSL
    smtp_server = smtpCreds['smtp_server']
    sender_email = smtpCreds['sender_email']
    receiver_emails = [smtpCreds['receiver_email'], receiverEmail]
    password = smtpCreds['password']

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, text)
        server.quit()


def GetSmtpCredentials():
    mailCredentials = 'mailCredentials.json'

    if not os.path.exists(mailCredentials):
        raise CannotSendAccountInfoToClientException()

    with open('mailCredentials.json') as f:
        json_data = json.load(f)
        tmp = json_data['smtp_server']
        tmp = json_data['sender_email']
        tmp = json_data['receiver_email']
        tmp = json_data['password']
        return json_data
