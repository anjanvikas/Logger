import cv2
import numpy as np
import MySQLdb
from datetime import datetime
import random
import pyprind

def getTotalSamples():
    return 20

def maxInDatabase():
    return 2147483648

def insertOrUpdate(identifier, name):
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    cmd = "SELECT * FROM People WHERE ID = '%s'" % str(identifier)
    cursor.execute(cmd)
    results = cursor.fetchall()
    try:
        if(results):
            cmd = "UPDATE People SET Name = '%s' WHERE ID = '%s'" % (str(name), str(identifier))
            cursor.execute(cmd)
        else:
            cmd = "INSERT INTO People(ID, Name) Values('%s', '%s')" % (str(identifier), str(name))
            cursor.execute(cmd)
        db.commit()
    except:
        db.rollback()
    db.close()

def main(name):
    random.seed(datetime.now())
    faceCascde = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    identifier = str(random.randint(1, maxInDatabase()))
    sample_number = 0
    insertOrUpdate(identifier, name)
    n = getTotalSamples()
    bar = pyprind.ProgBar(n, track_time = True, title = "Collecting Dataset")
    while (sample_number < n):
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascde.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sample_number += 1
            cv2.imwrite("dataSet/user."+str(identifier)+"."+str(sample_number)+".jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+h, y+w), (0, 255, 0), 2)
            cv2.waitKey(100)
            bar.update()
        cv2.imshow('Face Detect', img)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    name = raw_input('Enter employee name : ')
    main(name)
