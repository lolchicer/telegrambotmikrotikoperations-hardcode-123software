import sys
import json
import smtplib, ssl
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def ValidateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

def TrySendAccountInfoToClient(accountName, accountPassword, presharedKey, IP):
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
    return TrySendEmailToClient(accountName, "Доступ к VPN", body)


def TrySendEmailToClient(receiverEmail, subject, body):
    smtpCreds = TryGetSmtpCredentials()    
    if smtpCreds == False:
        return False
    try:
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
        return True
    except:
        return False

def TryGetSmtpCredentials():
    try:
        with open('mailCredentials.json') as f:
            json_data = json.load(f)
            tmp = json_data['smtp_server']
            tmp = json_data['sender_email']
            tmp = json_data['receiver_email']
            tmp = json_data['password']
            return json_data
    except (FileNotFoundError, KeyError):
        return False