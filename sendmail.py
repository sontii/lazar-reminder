import smtplib
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# list for recipients
emailRecipients = []
errorRecipient = []

# enviroment variables setup
xPath = os.getenv("XLSXPATH")
logPath = os.getenv("LOGFILEPATH")
envRecipients = os.getenv("EMAILRECIPIENTS")
errorRecipient.append(os.getenv("ERRORRECIPIENT"))
errorRecipientSTR = os.getenv("ERRORRECIPIENT")
envSender = os.getenv("SENDER")
envSmtpPass = os.getenv("SMTP_PASS")

# env list
for email in envRecipients.split(","):
   emailRecipients.append(email)

logging.basicConfig(filename=logPath, level=logging.INFO)

def main():
   try:
      with open(xPath, "rb") as f:
        df = pd.read_excel(f, skiprows=3, engine='openpyxl')
   except Exception as err:
      errorMail(err)
      logging.info(" "  + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Hiba a file megnyitásakor: " + f"{err}")
      exit(1)

   dateCompare = datetime.today() + timedelta(days=40)

   for index, row in df.iterrows():
      if row['Dátum'] < dateCompare:
         datum = row['Dátum'].strftime("%Y.%m.%d")
         okmany = row['Okmány']
         subject = f'{okmany} Lejáró okmány {datum}'
         body = f'Emlékeztető email lejáró okmányról.\n {datum} {okmany}'
         recipients = emailRecipients
         try:
            send_email(subject, body, recipients)
         except smtplib.SMTPException as e:
            logging.info(" " + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Nem sikerült elküldeni a levelet hiba: " + f"{e}")

   logging.info(" "  + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " sikeres küldés")

def errorMail(err):
   subject = 'Ertesito email hiba'
   body = MIMEText(f"Hiba - ellenőrizd a logot: \n {err}")
   recipients = errorRecipientSTR

   try:
      send_email(subject, body, recipients)
   except smtplib.SMTPException as e:
      logging.info(" " + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Nem sikerült elküldeni a levelet hiba: " + f"{e}")


def send_email(subject, body, recipients):
    msg = MIMEText(body.encode('utf-8'), "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = envSender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
       server.login('f.ferenc@lazarteam.hu', envSmtpPass)
       server.sendmail(envSender, recipients, msg.as_string())
    print("Üzenet elküldve!")


if __name__ == "__main__":
    main()
