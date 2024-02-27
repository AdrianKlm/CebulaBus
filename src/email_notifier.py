import smtplib
from email.message import EmailMessage
import json
import configparser

def load_config():
    cfg = configparser.ConfigParser()
    cfg.read('config/settings.ini')
    return cfg

def load_email_list():
    with open('data/emailList.json', 'r') as file:
        emails = json.load(file)
    return emails

def send_email(subject, content, recipient_emails):
    cfg = load_config()
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = cfg.get('Email', 'Login')
    msg['To'] = ", ".join(recipient_emails)
    print(msg)

    # with smtplib.SMTP_SSL(cfg.get('Email', 'Smtp')) as s:
    #     s.login(cfg.get('Email', 'Login'), cfg.get('Email', 'Password'))
    #     s.send_message(msg)

