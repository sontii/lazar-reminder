import smtplib
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime, timedelta
import logging


logging.basicConfig(filename="logfile.log", level=logging.INFO)


def main():
   try:
      df = pd.read_excel('/share0/menteni/common/Doks/emlekezteto/emlekezteto.xlsx', skiprows=3, engine='openpyxl')
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
   receivers = ['kassai.dora@lazarteam.hu, konyveles@lazarteam.hu']

   message = MIMEText(f'Emlékeztető email lejáró okmányról.\n {datum} {okmany}')

   message['From'] = 'ertesito@lazarteam.hu'
   message['To'] = 'kassai.dora@lazarteam.hu, konyveles@lazarteam.hu'
   message['Subject'] = f'{okmany} Lejáró okmány {datum}'

   try:
      smtpObj = smtplib.SMTP('192.168.103.100')
      smtpObj.sendmail(sender, receivers, message.as_string())
   except smtplib.SMTPException as e:
      logging.info(" " + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Nem sikerült elküldeni a levelet ", e)

def errorMail(err):
   sender = 'ertesito@lazarteam.hu'
   receivers = ['f.ferenc@lazarteam.hu']

   message = MIMEText(err)

   message['From'] = 'ertesito@lazarteam.hu'
   message['To'] = 'f.ferenc@lazarteam.hu'
   message['Subject'] = 'Nem található az excel'

   try:
      smtpObj = smtplib.SMTP('192.168.103.100')
      smtpObj.sendmail(sender, receivers, message.as_string())
   except smtplib.SMTPException:
      logging.info(" " + datetime.now().strftime('%Y.%m.%d %H:%M:%S') + " Nem sikerült elküldeni a levelet ")



if __name__ == "__main__":
    main()