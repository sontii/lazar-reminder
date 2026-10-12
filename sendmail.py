import smtplib
import sys
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# enviroment variables setup
xPath = os.getenv("XLSXPATH")
logPath = os.getenv("LOGFILEPATH")
emailRecipients = [email.strip() for email in os.getenv("EMAILRECIPIENTS").split(",")]
errorRecipients = [os.getenv("ERRORRECIPIENT")]
envSender = os.getenv("SENDER")
envSmtp = os.getenv("SMTP", "smtp.gmail.com")
envSmtpPort = int(os.getenv("SMTPPORT", "465"))
# Gmail login account; SENDER is an alias of it
envSmtpUser = os.getenv("SMTP_USER", "f.ferenc@lazarteam.hu")
envSmtpPass = os.getenv("SMTP_PASS")

logging.basicConfig(
   filename=logPath,
   encoding='utf-8',
   format='%(asctime)s %(levelname)s %(message)s',
   datefmt='%Y.%m.%d %H:%M:%S',
   level=logging.INFO,
)


def log_uncaught(exc_type, exc, tb):
   # Errors outside the handled cases would otherwise only reach stderr
   logging.critical("Váratlan hiba, a futás leállt", exc_info=(exc_type, exc, tb))
   errorMail(f"Váratlan hiba, a futás leállt: {exc}")
   sys.__excepthook__(exc_type, exc, tb)


sys.excepthook = log_uncaught


def main():
   try:
      with open(xPath, "rb") as f:
        df = pd.read_excel(f, skiprows=3, engine='openpyxl')
   except Exception as err:
      logging.error(f"Hiba a file megnyitásakor: {err}")
      errorMail(err)
      sys.exit(1)

   # Text or mistyped dates become NaT instead of breaking the comparison
   dates = pd.to_datetime(df['Dátum'], errors='coerce')
   dateCompare = datetime.today() + timedelta(days=40)

   sent = 0
   failed = []
   for index, row in df.iterrows():
      okmany = row['Okmány']
      if pd.isna(dates[index]):
         if not pd.isna(row['Dátum']) or not pd.isna(okmany):
            # Excel row number: 3 skipped rows + header + 1-based index
            # A mistyped date would otherwise silently stop the reminder forever
            failed.append(f"Hibás dátum a {index + 5}. sorban: {row['Dátum']!r} ({okmany})")
            logging.warning(failed[-1])
         continue
      if dates[index] < dateCompare:
         datum = dates[index].strftime("%Y.%m.%d")
         subject = f'{okmany} Lejáró okmány {datum}'
         body = f'Emlékeztető email lejáró okmányról.\n {datum} {okmany}'
         try:
            send_email(subject, body, emailRecipients)
            sent += 1
         except Exception as e:
            # Keep going so one failed mail does not block the other reminders
            logging.error(f"Nem sikerült elküldeni a levelet ({subject}): {e}")
            failed.append(f"{subject}: {e}")

   if failed:
      errorMail("Ellenőrizd az emlékeztető táblázatot / a levélküldést:\n" + "\n".join(failed))
   logging.info(f"Futás vége: {sent} emlékeztető elküldve, {len(failed)} hiba")


def errorMail(err):
   subject = 'Ertesito email hiba'
   body = f"Hiba - ellenőrizd a logot: \n {err}"

   try:
      send_email(subject, body, errorRecipients)
   except Exception as e:
      logging.error(f"Hibalevél küldése sikertelen: {e}")


def send_email(subject, body, recipients):
    msg = MIMEText(body.encode('utf-8'), "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = envSender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL(envSmtp, envSmtpPort) as server:
       server.login(envSmtpUser, envSmtpPass)
       server.sendmail(envSender, recipients, msg.as_string())
    logging.info(f"Levél elküldve: {subject}")


if __name__ == "__main__":
    main()
