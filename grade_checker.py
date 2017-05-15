#!/usr/bin/python3

from moodle_html_parser import *
import requests
import difflib
import os
import smtplib

def loginAndGetPage(user, password):
    url = 'https://ay16.moodle.umn.edu'
    s = requests.session()
    login_data = { 'j_username': user,
                   'j_password': password,
                   '_eventId_proceed': '',
                 }

    # Get redirected to login page
    r = s.post(url, data=login_data)
    # Login
    m = s.post("https://login.umn.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1", data=login_data)

    # Parse the login keys that are then sent to moodle, and 'login' to moodle
    fb = FormHTMLParser()
    fb.feed(m.text)
    form = fb.forms[0]
    data2 = {}
    rs = form.inputs[0]
    data2[rs['name']] = rs['value']
    rs = form.inputs[1]
    data2[rs['name']] = rs['value']
    a = s.post(form.action, data=data2)
    return a.text

def updateGradeFile(text):
    f = open("grades.txt", "w+")
    f.write(text)
    f.close() 

def sendNotification(username):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    login = "ratchet.mail.bot@gmail.com"
    password = open("email_password.txt").read()
    server.login(login, password)
    to = username + "@umn.edu"
    subject = "Grade Update"
    msg = "Your grade has been changed. Check moodle"
    message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (login, to, subject, msg)
    
    server.sendmail(login, to, message)
    
    
    
def main():
    # Read in username and password
    f = open("user_info.txt")
    text = f.read().strip()
    f.close()
    s = text.split()
    user = s[0]
    password = s[1]
    

    # login and get the moodle page
    page = loginAndGetPage(user, password)
    
    # parse the file
    parser = MoodleGradeParser()
    parser.feed(page)
    parser.close()
    new = parser.getData()

    # see if past record of grades exists
    if 'grades.txt' not in os.listdir():
        updateGradeFile(new)
        return
    
    # Compare to the last record of grades
    f = open("grades.txt")
    old = f.read()
    f.close()
    d = difflib.SequenceMatcher(None, old, new)
    if d.ratio() != 1.0:
        print("change in grade")
        sendNotification(user)
        updateGradeFile(new)

    else:
        print("no change in grade")

    return

if __name__ == '__main__':
    main()
