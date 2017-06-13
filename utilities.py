import MySQLdb

def getIdentifier(name):
    db = MySQLdb.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    cmd = "SELECT * FROM People WHERE Name = '%s'" % str(name)
    cursor.execute(cmd)
    profile = cursor.fetchone()
    db.close()
    return profile[0]
