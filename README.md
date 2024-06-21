# Fridrich Ferenc

## Lazarteam - weekly reminder email from excel

---

## Description:

This application stand for send weekly email from expiring documents
Written in python.

---

### **How to use:**

Use with cron weekly run.
If the apllication doesn't find the xlsx file, it will send email to the administrator
and append the log file.

---

#### **Requirements:**

examine Dockerfile
useing 3.9-alpine 
- docker build -t reminder-email-script:latest .
- run with start-docker.sh

---

### **Files and folders:**

- sendemail.py
- README.md <- you are here
- reqirement.txt
- .env
- logs/log

---

