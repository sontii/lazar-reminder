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
envSMTP = os.getenv("SMTP")

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
         sendMail(datum, okmany)

   logging.info(" "  + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " sikeres küldés")

def sendMail(datum, okmany):
   sender = envSender
   recipients = emailRecipients

   message = MIMEText(f'Emlékeztető email lejáró okmányról.\n {datum} {okmany}')

   message['From'] = envSender
   message['To'] = ", ".join(recipients)
   message['Subject'] = f'{okmany} Lejáró okmány {datum}'

   try:
      smtpObj = smtplib.SMTP(envSMTP)
      smtpObj.sendmail(sender, recipients, message.as_string())
   except smtplib.SMTPException as e:
      logging.info(" " + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Nem sikerült elküldeni a levelet hiba: " + f"{e}")

def errorMail(err):
   sender = envSender
   recipients = errorRecipient

   message = MIMEText( f"Hiba - ellenőrizd a logot: \n {err}")

   message['From'] = envSender
   message['To'] = errorRecipientSTR
   message['Subject'] = 'Ertesito email hiba'

   try:
      smtpObj = smtplib.SMTP(envSMTP)
      smtpObj.sendmail(sender, recipients, message.as_string())
   except smtplib.SMTPException as e:
      logging.info(" " + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Nem sikerült elküldeni a levelet hiba: " + f"{e}")

if __name__ == "__main__":
    main()
