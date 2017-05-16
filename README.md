# Grade Notifier App

## Description

Python script I built to notify me via email when my grades change. Runs every 10 minutes on my home server and does the following steps:

1. Logs in to the UMN account using the user / password specified in user_info.txt
2. Downloads the Moodle page homepage that should have the grades preview on it
3. Compares it to the last record of the grades it pulled down
4. If its different, it sends an email to the user specifying which classes were added / changed. Also specifies what the grade used to be, and what is is now, and hyperlinks the detailed grade page.
5. Updates the record of the grades to reflect the new download

Timed functionality is done via cron job. Rest is done using python libraries.

## Installation and Usage

To run this, you need to do the following:
1. Add a file called "user_info.txt" in the same directory as the program. Only add the following on the first line: [user] [password]
2. It should be able to run now anything you use the one of the following commands:
> ./grade_checker.py

or

> python3 grade_checker.py

It will run and email you if your grade changed since last time run.
4. Set it up so that this script auto runs however frequently you want your grades to be checked (see below for details)

### Allowing this script
Most gmail accounts will view this script the first time it tries to email you as suspicious. If that happens, it won't let the email through, but it will send you an email saying "if this is you, allow access by clicking this link". It's fine, just follow the link and allow access. It will work on future tries. The first time the program is run (when it doesn't detect a past record of grades saved in grades.txt) it will try to send a welcome email

The first time you run it, just downloads your grades into a file called: "grades.txt". Running it successive times will detect changes in your grades

#### Making it auto run on linux machines with Cron
If you want to make it automatically run every so often, I used Cron to do that. Cron is already installed on most linux / ubuntu machines. To set it up, just do the following on a linux computer that is always on:
1. crontab -e
2. Add in a line: */10 * * * * cd /absolute/path/to/program/directory/ && python3 grade_checker.py > /dev/null

Now every 10 minutes it will run
