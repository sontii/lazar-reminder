# Fridrich Ferenc

## Lazarteam - weekly reminder email from excel

---

## Description:

This application stand for send weekly email from expiring documents
Written in python.

---

### **How to use:**

Use with cron weekly run (Monday 05:00).
Reads xls/emlekezteto.xlsx (header in row 4: Dátum, Okmány) and sends one email
per document expiring within 40 days (already expired ones included) to EMAILRECIPIENTS.

Errors are logged to logs/log and emailed to ERRORRECIPIENT:
- xlsx missing / cannot be opened
- a reminder mail could not be sent (the other reminders still go out)
- a row with an invalid date (the reminder for it would never be sent otherwise)
- any unexpected error

---

#### **Requirements:**

examine Dockerfile
using python:3.11-slim
- run with start-docker.sh (builds the image, then runs it)
- the code is baked into the image, only .env, xls/ and logs/ are mounted,
  so code changes need a rebuild (start-docker.sh always rebuilds)

.env: LOGFILEPATH, XLSXPATH, EMAILRECIPIENTS (comma separated), ERRORRECIPIENT,
SENDER, SMTP, SMTPPORT, SMTP_PASS, optional SMTP_USER (Gmail login, default f.ferenc@lazarteam.hu)

---

### **Files and folders:**

- sendmail.py
- README.md <- you are here
- requirements.txt
- .env
- logs/log

---

