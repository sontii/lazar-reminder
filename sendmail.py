import smtplib
import pandas as pd
from io import StringIO


def main():
   df = pd.read_excel('emlekezteto.xlsx', skiprows=4)
   print(df)


def sendMail():
   sender = 'ertesito@lazarteam.hu'
   receivers = ['f.ferenc@lazarteam.hu']

   message = """From: Havi ertesito <ertesito@lazarteam.hu>
   To: To konyveles <f.ferenc@lazarteam.hu>
   Subject: Havi emlekeztete email

   This is a test e-mail message.
   """

   try:
      smtpObj = smtplib.SMTP('localhost')
      smtpObj.sendmail(sender, receivers, message)
      print("Successfully sent email")
   except smtplib.SMTPException:
      print("Error: unable to send email")



if __name__ == "__main__":
    main()