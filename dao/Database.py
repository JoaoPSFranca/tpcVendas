import mysql.connector

class Database:
   def __init__(self):
       self.server=""
       self.database=""
       self.password=""
       self.user=""
       self.port=3306
       self.pointer =""

   def openConnection(self):
      self.connect = mysql.connector.connect(host=self.server,
                                 database=self.database,
                                 user=self.user,
                                 passwd=self.password,
                                 port=self.port)
      self.pointer = self.connect.cursor()

   def selectQuery(self, entry):
      self.pointer.execute(entry)
      reply = self.pointer.fetchall()
      return reply

   def executeQuery(self, entry, data):
       self.pointer.execute(entry, data)

   def execute(self, entry):
       self.pointer.execute(entry)

   def save(self):
      self.connect.commit()

   def discard(self):
      self.connect.rollback()

   def setting(self, ho, us, se, db, po=3306):
       self.server = ho
       self.user = us
       self.password = se
       self.database = db
       self.port = po

   def showResult(self, entry):
       for i in entry:
           print(i)