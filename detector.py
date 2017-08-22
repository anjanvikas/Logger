import cv2
import numpy as np
import os
import MySQLdb
import utilities
from datetime import datetime

def getTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getName(profile):
    return str(profile[1])

def getProfile(identifier):
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    cmd = "SELECT * FROM People WHERE ID = '%s'" % str(identifier)
    cursor.execute(cmd)
    profile = cursor.fetchone()
    db.close()
    return profile

def getNextState(name):
    empID = utilities.getIdentifier(name)
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    cmd = "SELECT t1.* FROM empLog t1 WHERE (t1.time = (SELECT max(t2.time) FROM empLog t2 WHERE t2.empID = t1.empID) AND empID = '%s');" % str(empID)
    cursor.execute(cmd)
    profile = cursor.fetchone()
    if(profile == None):
        return 0
    elif(profile[3]):
        return 0
    return 1

def setLog(name):
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    empID = utilities.getIdentifier(name)
    logTime = getTime()
    nextState = getNextState(name)
    try:
        cmd = "INSERT INTO empLog(empID, time, state) VALUES('%s', '%s', '%s');" % (str(empID), str(logTime), str(nextState))
        cursor.execute(cmd)
        db.commit()
        if(nextState == 0):
            print 'Welcome back ' + str(name)
        else:
            print 'See you soon ' + str(name)
    except:
        db.rollback()
    db.close()


def main():
    faceCascde = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    rec = cv2.createLBPHFaceRecognizer()
    rec.load(os.path.join("recognizer", "trainingData.yml"))
    font = cv2.FONT_HERSHEY_SIMPLEX
    exitFlag = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascde.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+h, y+w), (0, 255, 0), 2)
            identifier, conf = rec.predict(gray[y:y+h, x:x+w])
            profile = getProfile(identifier)
            name = getName(profile)
            if(profile != None and conf < 100):
                cv2.putText(img, name, (x, y+h), font, 1, (255, 0, 0), 2, cv2.CV_AA)
                setLog(name)
                exitFlag = 1
                break
            else:
                cv2.putText(img, "Unknown", (x, y+h), font, 1, (255, 0, 0), 2, cv2.CV_AA)
        cv2.imshow('Face Detect', img)
        if(((cv2.waitKey(30) & 0xFF) == 27) or exitFlag == 1):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
