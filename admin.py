import datetime
import utilities
import MySQLdb
import matplotlib.pyplot as plt
import dataSetCreator
import trainer
import os

def addEmployee(name):
    dataSetCreator.main(name)
    trainer.main()
    print name + ' has been successfully added'

def removeImages(path, empID):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    imagePaths.remove('dataSet/.keep')
    empID = int(empID)
    for imagePath in imagePaths:
        identifier = int(os.path.split(imagePath)[-1].split('.')[1])
        if(empID == identifier):
            os.remove(imagePath)

def removeEmployee(name):
    empID = utilities.getIdentifier(name)
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    cmd = "DELETE FROM empLog WHERE empID = '%s'" % (str(empID))
    cursor.execute(cmd)
    db.commit()
    cmd = "DELETE FROM People WHERE ID = '%s'" % (str(empID))
    cursor.execute(cmd)
    db.commit()
    db.close()
    path = "dataSet"
    removeImages(path, empID)
    files = os.listdir(path).remove('.keep')
    if(files):
        trainer.main()
    else:
        open(os.path.join('recognizer', 'trainningData.yml'), 'w').close()    

def plotOneEmp(name, hrs):
    plt.plot(range(1, 13), hrs, 'ro')
    plt.title('Statistics of ' + name)
    plt.xlabel('Months')
    plt.ylabel('Number of hours')
    plt.show()

def getHours(name, year):
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    try:
        cmd = "INSERT INTO tmp SELECT empID, DATE(time) day, SEC_TO_TIME(SUM(TIMESTAMPDIFF(SECOND, time, (SELECT IFNULL(MIN(time),NOW()) FROM empLog b WHERE b.empid = a.empid AND b.time  > a.time AND b.state = 1)))) date_worked FROM empLog a WHERE state=0 GROUP BY empID, DATE(time);"
        cursor.execute(cmd)
        empID = utilities.getIdentifier(name)
        hrs = []
        for month in range(1, 13):
            cmd = "SELECT * FROM tmp WHERE (empID = '%s' AND (`day` >= '%s' AND `day` <= '%s'));"% (str(empID), str(year)+'-'+str(month)+'-01', str(year)+'-'+str(month)+'-31')
            cursor.execute(cmd)
            profile = cursor.fetchone()
            if(profile):
                hrs.append(profile[2]/3600.0)
            else:
                hrs.append(0.0)
        cmd = "TRUNCATE tmp;"
        cursor.execute(cmd)
        return hrs
    except:
        db.rollback()
    db.close()

def plot():
    name = raw_input("Enter the employee name : ")
    year = raw_input("Enter the year : ")
    plotOneEmp(name, getHours(name, year))

def deleteRecords(tillDate):
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    cmd = "DELETE FROM empLog WHERE DATE(time) < '%s'" % str(tillDate)
    cursor.execute(cmd)
    db.commit()
    db.close()

def setDeleteRecords():
    tillDate = raw_input('Enter the date before which the records has to be deleted : ')
    deleteRecords(tillDate)
    print 'Records have been successfully removed'

def workedTime(empName, startDate, endDate):
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    try:
        cmd = "INSERT INTO tmp SELECT empID, DATE(time) day, SEC_TO_TIME(SUM(TIMESTAMPDIFF(SECOND, time, (SELECT IFNULL(MIN(time),NOW()) FROM empLog b WHERE b.empid = a.empid AND b.time  > a.time AND b.state = 1)))) date_worked FROM empLog a WHERE state=0 GROUP BY empID, DATE(time);"
        cursor.execute(cmd)
        empID = utilities.getIdentifier(empName)
        cmd = "SELECT * FROM tmp WHERE (empID = '%s' AND (`day` >= '%s' AND `day` <= '%s'));" % (str(empID), str(startDate), str(endDate))
        cursor.execute(cmd)
        profile = cursor.fetchall()
        workedSeconds = 0
        for row in profile:
            workedSeconds = workedSeconds + row[2]
        print "Total time worked : " + "{:0>8}".format(datetime.timedelta(seconds = workedSeconds))
        cmd = "TRUNCATE tmp;"
        cursor.execute(cmd)
    except:
        db.rollback()
    db.close()

def getWorkedTime():
    name = raw_input('Enter the employee name : ')
    startDate = raw_input('Enter the query start date : ')
    endDate = raw_input('Enter the query end date : ')
    workedTime(name, startDate, endDate)

def main():
    print '1. Add employee'
    print '2. Remove employee'
    print '3. Get number of hours worked by an employee'
    print '4. Remove old records'
    print '5. Plot statistics curve of an employee'
    choice = input()
    if(choice == 1):
        name = raw_input('Enter employee name : ')
        addEmployee(name)
    elif(choice == 2):
        name = raw_input('Enter employee name : ')
        removeEmployee(name)
    elif(choice == 3):
        getWorkedTime()
    elif(choice == 4):
        setDeleteRecords()
    elif(choice == 5):
        plot()

if __name__ == '__main__':
    main()
