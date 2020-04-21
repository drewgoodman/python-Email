import smtplib

from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.environ.get('SENDER_EMAIL')
sender_password = os.environ.get('SENDER_PASSWORD')
receiver_email = os.environ.get('RECEIVER_EMAIL')


smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtpObj.ehlo()
# smtpObj.starttls()
smtpObj.login(sender_email, sender_password)
smtpObj.sendmail(sender_email,receiver_email, "Subject: This is a test!\nThe first of many!")
smtpObj.quit()
