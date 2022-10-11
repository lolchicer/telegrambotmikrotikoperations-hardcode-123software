import smtplib
import ssl
import exceptions
import configFunctions
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def SendAccountInfoToClient(accountName, accountPassword, presharedKey, IP):
    body = f"""Добрый день!

Для вас была создана учетная запись для подключения к VPN по адресу {IP} :

Логин: {accountName}
Пароль: {accountPassword}

Настройка нового подключения или сети
Подключение к рабочему месту
Создать новое подключение
Использовать мое подключение к интернету (VPN)
Интернет-адрес: {IP}

Вкладка Безопасность:
Тип VPN: L2TP IPSec VPN
Дополнительные параметры: для проверки подлинности использовать предварительный ключ. В нашем случае это: {presharedKey} (IP - IPSec - Peers)

Здесь же, в группе "Проверка подлинности", оставляем только CHAP v2"""
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendDisablingNotificationToClient(accountName, IP):
    body = f"""Добрый день!

Работа вашей учетной записи для подключения к VPN по адресу {IP} была приостановлена."""
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendEnablingNotificationToClient(accountName, accountPassword, IP):
    body = f"""Добрый день!

Работа вашей учетной записи для подключения к VPN по адресу {IP} была восстановлена.

Новый пароль: {accountPassword}"""
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendNewPasswordToClient(accountName, accountPassword, IP):
    body = f"""Добрый день!
    
Пароль вашей учётной записи {accountName} для подключения к VPN по адресу {IP} был изменён:
    
{accountPassword}"""
    return SendEmailToClient(accountName, "Доступ к VPN", body)


def SendEmailToClient(receiverEmail, subject, body):
    smtpCreds = configFunctions.GetMailCredentials()

    port = 465  # For SSL
    smtp_server = smtpCreds['smtp_server']
    sender_email = smtpCreds['sender_email']
    receiver_emails = [receiverEmail]
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
