import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

def sendMail(html, asunto, para):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = os.getenv('EMAIL_HOST_USER')
    msg['To'] = para
    msg.attach(MIMEText(html, 'html'))
    print(para)
    
    try:
        server = smtplib.SMTP(os.getenv('EMAIL_HOST'), os.getenv('EMAIL_PORT'))
        server.connect(os.getenv('EMAIL_HOST'), os.getenv('EMAIL_PORT'))
        server.login(os.getenv('EMAIL_HOST_USER'), os.getenv('EMAIL_HOST_PASSWORD'))
        server.sendmail(os.getenv('EMAIL_HOST_USER'), para, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error al conectar al servidor SMTP:", str(e))
        