import MySQLdb

# open database connection
db = MySQLdb.connect('localhost','root','pass','test')

# prepare a cursor
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")
# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data

# cursor.execute("select name, email_private,id_number  from Person")
# data = cursor.fetchall()

# for each in data:
#     for i in each:
#         print i + ' ',
#     print '\n'
cmd = '''INSERT INTO `test`.`zhilianTest` (`name`, `ID_no`, `email_private`, `email_work`, `mobile`, `resume_ID`, `person_INFO`, `resume_update_time`, `intention`, `self_evaluation`, `work_experience`, `project_experience`) VALUES ('fads w', 'erq', 'werqw', 'qwrefwadsfsa', 'fast', 'fast', 'fads', 'ter34wf', 'sad', 'asd', 'hbdtf', 'asd')'''
cursor.execute(cmd)

# 下面这两句必须有
cursor.close()
# commit之后才能真正地将数据写入数据库！！！！！！
db.commit() # 提交事务

# disconnect from server
db.close()
