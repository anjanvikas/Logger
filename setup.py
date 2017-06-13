import MySQLdb

def setupDatabase():
    db = MySQLdb.connect("localhost", "root", "root")
    cursor = db.cursor()
    cmd = "CREATE DATABASE IF NOT EXISTS TESTBASE;"
    cursor.execute(cmd)
    db.close()

def createTables():
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    cmd = "CREATE TABLE IF NOT EXISTS `People` (`ID` int(11) NOT NULL, `Name` varchar(50) NOT NULL, `empID` varchar(20) DEFAULT '', PRIMARY KEY (`ID`));"
    cursor.execute(cmd)
    cmd = "CREATE TABLE IF NOT EXISTS `empLog` (`ID` int(11) NOT NULL AUTO_INCREMENT, `empID` varchar(20) DEFAULT '', `time` datetime DEFAULT NULL, `state` int(11) DEFAULT NULL, PRIMARY KEY (`ID`));"
    cursor.execute(cmd)
    cmd = "CREATE TABLE IF NOT EXISTS `tmp` (`empID` int(11) DEFAULT NULL, `day` date DEFAULT NULL, `sec` int(11) DEFAULT NULL);"
    cursor.execute(cmd)
    db.close()

def main():
    setupDatabase()
    createTables()

if __name__ == '__main__':
    main()
