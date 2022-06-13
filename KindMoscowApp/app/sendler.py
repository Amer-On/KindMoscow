from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

server = smtplib.SMTP_SSL('smtp.mail.ru')
server.set_debuglevel(1)


def connect():
    global server
    password = "R4w9KuD24MhUGrMYhgvJ"
    server.login("noreply.dobrayaMoskva@mail.ru", password)
    server.auth_plain()


def send_message(to: str, code: str):
    global server
    if "recovery" not in code:
        message = f"Для подтверждения электронной почты и завершения " \
                  f"процесса регистрации, пройдите, пожалуйста, по " \
                  f"ссылке: {code}\n\n\nЕсли вы получили это письмо по " \
                  f"ошибке, проигнорируйте его."
    else:
        message = f"Для восстановления пароля, перейдите по этой ссылке:" \
                  f"{code}\n\n\nЕсли вы получили это письмо по " \
                  f"ошибке, проигнорируйте его."
    msg = MIMEMultipart()
    msg['Subject'] = "Подтверждение регистрации"
    msg.attach(MIMEText(message, 'plain'))
    server.sendmail("noreply.dobrayaMoskva@mail.ru", to, msg.as_string())
