import smtplib
import csv
import io



with io.open('emlekezteto.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)



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