from moodlegradeparser import MoodleGradeParser
import difflib
import os
import smtplib

def updateGradeFile(text):
    f = open("grades.txt", "w+")
    f.write(text)
    f.close() 

def sendNotification():
    if True:
        return
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    login = "ratchet.mail.bot@gmail.com"
    password = open("password.txt").read()
    server.login(From, password)
    to = "tyler147@umn.edu"
    message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (login, to, subject, msg)
    
    server.sendmail(login, to, message)
    
    
    
def main():
    # download file...

    # parse the file
    parser = MoodleGradeParser("moodle.html")
    parser.parse()
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
        sendNotification()
        updateGradeFile(new)

    else:
        print("no change in grade")

    return

