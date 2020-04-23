
# Sends the first 12 articles on ScreenRant's homepage in an email.

import smtplib, os, requests
from dotenv import load_dotenv
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup


load_dotenv()

headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
res = requests.get("http://screenrant.com", headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'html.parser')
articles = soup.find_all(class_="bc-title-link", limit=12)
date = date.today().strftime("%B %d")

sender_email = os.environ.get('SENDER_EMAIL')
sender_password = os.environ.get('SENDER_PASSWORD')
receiver_email = os.environ.get('RECEIVER_EMAIL')


msg = MIMEMultipart('alternative')
msg['Subject'] = "ScreenRant Articles for " + date + "\n\nToday"
msg['From'] = sender_email
msg['To'] = receiver_email

content_text = "Here are your daily ScreenRant Articles:\n\n"
content_html = """\
    <html>
    <head></head>
    <body>
    <p>Here are your daily ScreenRant Articles:</P>
    <hr>
    <ol>
"""

for article in articles:
    link = "<a href='https://screenrant.com" + article.get('href') + "'>" + article.contents[0] + "</a>"
    content_html += "<li>"+ link + "</li>"
    content_text += article.contents[0] + " - https://screenrant.com" + article.get('href') + "\n\n"

content_html += "</ol></body></html>"


msg.attach(MIMEText(content_text,"plain"))
msg.attach(MIMEText(content_html,"html"))


smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtpObj.ehlo()
smtpObj.login(sender_email, sender_password)
smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
smtpObj.quit()
