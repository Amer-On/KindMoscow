from fastapi import FastAPI, Request
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
import smtplib
import secrets

# configuration variables
API_LOGIN = "bos0fThe&ym"
API_PASSWORD = "co5T@r1zat!0N"

EMAIL = "noreply.dobrayaMoskva@mail.ru"
PASSWORD = "R4w9KuD24MhUGrMYhgvJ"


# fast api init
app = FastAPI()

# security to restrict the intervention from outside
security = HTTPBasic()

# smtp server init
server = smtplib.SMTP_SSL('smtp.mail.ru')
server.set_debuglevel(1)

# connect to smtp server
server.login(EMAIL, PASSWORD)
server.auth_plain()


TYPES = ["confirm-recovery", "confirm"]


def get_current_cridentials(credentials: HTTPBasicCredentials = Depends(security)) -> HTTPBasicCredentials:
    correct_username = secrets.compare_digest(credentials.username, API_LOGIN)
    correct_password = secrets.compare_digest(credentials.password, API_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.get("/")
async def root():
    return "Welcome to Kind Moscow API. The use is encrypted, so you can use this API only if you know the login&password"

@app.get("/send_email/{recipient_email}/{mode}/{code}")
async def send_email(recipient_email: str, mode: str, code: str, request: Request, credentials: HTTPBasicCredentials = Depends(get_current_cridentials)):
	if mode in TYPES:		
		link = f"http://{request.client.host}:80/{mode}/{code}"
		if mode == "confirm":
			subject = "Подтверждение регистрации"
			message = f"Для подтверждения электронной почты и завершения " \
                  f"процесса регистрации, пройдите, пожалуйста, по " \
                  f"ссылке: {link}\n\n\nЕсли вы получили это письмо по"  \
                  f"ошибке, проигнорируйте его."
		else:
			subject = "Изменение пароля"
			message = f"Для восстановления пароля, перейдите по этой ссылке: " \
                  f"{link}\n\n\nЕсли вы получили это письмо по " \
                  f"ошибке, проигнорируйте его."

		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg.attach(MIMEText(message, 'plain'))
		server.sendmail(EMAIL, recipient_email, msg.as_string())
		return "OK"

	else:
		return "inexistant mode"
