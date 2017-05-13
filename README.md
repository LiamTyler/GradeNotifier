# Grade Notifier App

## Description

Python script to notify me via email when my grades change. Runs every 10 minutes on my home server and does the following steps:

1. Logs in to my UMN account
2. Downloads the Moodle page that has my grades on it
3. Compares it to the last record of the grades
4. If its different, it sends me an email, which my phone is synched to. Then updates the record of the grades

Timed functionality is done via cron job. Rest is done using python libraries.
