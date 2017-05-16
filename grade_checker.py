#!/usr/bin/python3

from moodle_html_parser import *
import requests
import difflib
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

def sendFirstEmail(user, password):
    html = """\
            <html>
                <head></head>
                <body>
                    <p>Thanks for using the GradeNotifer script! If you are seeing this email, it means that this script is allowed to email you, and you do not have to do anything to allow it access. Now you can go be productive instead of habitually checking your grades, mainly after finals. Woo!</p>
                </body>
            </html>"""
    sendNotification(user, password, html)

def createHtmlMessage(added, changed):
    style = """\
            <style>
                table, th, td{
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                table {
                    width: auto;
                }
                caption {
                    font-weight: bold;
                }
            </style>
            """
    added_html = ""
    if (len(added) != 0):
        added_html = """\
                <table>
                    <caption>Added Classes</caption>
                    <tr>
                        <th>Class</th>
                        <th>Grade</th>
                    </tr>
                    """
        for c in added:
            added_html += """\
                    <tr>
                        <td><a href='%s'>%s</a></td>
                        <td>%s</td>
                    </tr>\n""" % (c[2], c[0], c[1])
        added_html += "</table>\n<br>\n"

    changed_html = ""
    if (len(changed) != 0):
        changed_html = """\
                <table>
                    <caption>Changed Classes</caption>
                    <tr>
                        <th>Class</th>
                        <th>Old Grade</th>
                        <th>New Grade</th>
                    </tr>
                    """
        for c in changed:
            changed_html += """\
                    <tr>
                        <td><a href='%s'>%s</a></td>
                        <td>%s</td>
                        <td>%s</td>
                    </tr>\n""" % (c[3], c[0], c[1], c[2])
        changed_html += "</table>\n<br>\n"

    html = """\
            <html>
                <head>%s</head>
                <body>
                    <p>There has been a change in your grades. Here is the <a href="https://ay16.moodle.umn.edu">Moodle Homepage</a>, And here were the changes in your grades:</p>
                    %s %s<br>
                </body>
            </html>""" % (style, added_html, changed_html)
    return html

def sendNotification(username, password, html):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    login = username + "@umn.edu"
    server.login(login, password)

    msg = MIMEMultipart('alternative')
    subject = "Grade Update"
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = login
    ret = MIMEText(html, 'html')
    msg.attach(ret)
    
    #server.sendmail(login, login, message)
    server.sendmail(login, login, msg.as_string())
    
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
    links = parser.getLinks()

    # see if past record of grades exists
    if 'grades.txt' not in os.listdir():
        print("First time running script. Recording grades and sending welcome email.")
        updateGradeFile(new)
        sendFirstEmail(user, password)
        return
    
    # Compare to the last record of grades
    f = open("grades.txt")
    old = f.read().strip()
    f.close()
    old_arr = old.split('\n')
    old_classes = []
    old_grades = []
    for line in old_arr:
        s = line.split(' : ')
        old_classes.append(s[0])
        old_grades.append(s[1])

    new_arr = new.strip().split('\n')
    new_classes = []
    new_grades = []
    for line in new_arr:
        s = line.split(' : ')
        new_classes.append(s[0])
        new_grades.append(s[1])

    added = []
    changed = []
    cl = len(old_classes)
    for c in range(len(new_classes)):
        old_class = ''
        new_class = new_classes[c]
        new_grade = new_grades[c]

        i = 0
        while i < cl and new_class != old_classes[i]:
            i += 1
        if i == cl:
            added.append([new_class, new_grade, links[c]])
            continue

        old_class = old_classes[i]
        old_grade = old_grades[i]

        if old_grade != new_grade:
            changed.append([new_class, old_grade, new_grade, links[c]])

    if len(added) != 0 or len(changed) != 0:
        print("change in grade")
        html = createHtmlMessage(added, changed)
        sendNotification(user, password, html)
        updateGradeFile(new)

    else:
        print("no change in grade")

    return

if __name__ == '__main__':
    main()
