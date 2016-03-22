import MySQLdb

# open database connection
db = MySQLdb.connect('localhost','root','passW0rd','test')

# prepare a cursor
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")
# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data

cursor.execute("select name, email_private,id_number  from Person")
data = cursor.fetchall()

for each in data:
    for i in each:
        print i + ' ',
    print '\n'

# disconnect from server
db.close()
