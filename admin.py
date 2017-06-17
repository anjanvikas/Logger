import datetime
import utilities
import MySQLdb

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
    choice = input("1. Get number of hours worked by an employee\n2. Delete old records\n")
    if(choice == 1):
        getWorkedTime()
    elif(choice == 2):
        setDeleteRecords()

if __name__ == '__main__':
    main()
