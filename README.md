# Grade Notifier App

## Description

Python script I built to notify me via email when my grades change. Runs every 10 minutes on my home server and does the following steps:

1. Logs in to my UMN account
2. Downloads the Moodle page that has my grades on it
3. Compares it to the last record of the grades
4. If its different, it sends me an email, which my phone is synched to. Then updates the record of the grades

Timed functionality is done via cron job. Rest is done using python libraries.

## Installation and Usage

To run this, you need to do the following:
1. Add a file called "user_info.txt" in the same directory as the program. Only add the following on the first line: [user] [password]
2. It should be able to run now anything you use the one of the following commands:
> ./grade_checker.py

or

> python3 grade_checker.py

The first time you run it, just downloads your grades into a file called: "grades.txt". Running it successive times will detect changes in your grades

#### Making it auto run on linux machines with Cron
If you want to make it automatically run every so often, I used Cron to do that. Cron is already installed on most linux / ubuntu machines. To set it up, just do the following on a linux computer that is always on:
1. crontab -e
2. Add in a line: */10 * * * * cd /absolute/path/to/program/directory/ && python3 grade_checker.py > /dev/null

Now every 10 minutes it will run
