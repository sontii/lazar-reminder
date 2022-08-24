import smtplib
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import os

load_dotenv()

xPath = os.getenv("XLSXPATH")

logging.basicConfig(filename="logfile.log", level=logging.INFO)


def main():
   try:
      df = pd.read_excel(f'{xPath}', skiprows=3, engine='openpyxl')
   except Exception as err:
      errorMail(err)
      logging.info(" "  + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " " + err)
      exit(1)   

   dateCompare = datetime.today() + timedelta(days=40)
 
   for index, row in df.iterrows():
      if row['Dátum'] < dateCompare:
         datum = row['Dátum'].strftime("%Y.%m.%d")
         okmany = row['Okmány']
         sendMail(datum, okmany)

def sendMail(datum, okmany):
   sender = 'ertesito@lazarteam.hu'
   recipients = ['kassai.dora@lazarteam.hu, konyveles@lazarteam.hu']

   message = MIMEText(f'Emlékeztető email lejáró okmányról.\n {datum} {okmany}')

   message['From'] = 'ertesito@lazarteam.hu'
   message['To'] = ", ".join(recipients)
   message['Subject'] = f'{okmany} Lejáró okmány {datum}'

   try:
      smtpObj = smtplib.SMTP('192.168.103.100')
      smtpObj.sendmail(sender, recipients, message.as_string())
   except smtplib.SMTPException as e:
      logging.info(" " + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Nem sikerült elküldeni a levelet hiba: " + e)

def errorMail(err):
   sender = 'ertesito@lazarteam.hu'
   recipients = ['f.ferenc@lazarteam.hu']

   message = MIMEText(err)

   message['From'] = 'ertesito@lazarteam.hu'
   message['To'] = 'f.ferenc@lazarteam.hu'
   message['Subject'] = 'Ertesito email hiba'

   try:
      smtpObj = smtplib.SMTP('192.168.103.100')
      smtpObj.sendmail(sender, recipients, message.as_string())
   except smtplib.SMTPException as e:
      logging.info(" " + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Nem sikerült elküldeni a levelet hiba: " + e)



if __name__ == "__main__":
    main()