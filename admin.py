import datetime
import utilities
import MySQLdb

def setTable(empName, startDate, endDate):
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

def main():
    name = raw_input('Enter the employee name : ')
    startDate = raw_input('Enter the query start date : ')
    endDate = raw_input('Enter the query end date : ')
    setTable(name, startDate, endDate)

if __name__ == '__main__':
    main()
