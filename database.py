import sqlite3


class CommentStorage(object):
	def __init__(self, path):
		self.connection = sqlite3.connect(path) 
		self.cursor = self.connection.cursor()
         
		 
 
	def Close(self):
		self.cursor.close()
		self.connection.close()
		
	def CreateDb(self):
	    
		query = """CREATE TABLE amazonDB
					(id INTEGER PRIMARY KEY, rating INTEGER, author TEXT,  date DATETIME, text TEXT, emotion TEXT )"""
		self.cursor.execute(query)
		self.connection.commit()

		
         
	def AddComment(self, rating, author, date, text, emotion):

		self.cursor.execute("""INSERT INTO amazonDB
					            VALUES (?,?,?,?,?,?)""", (None, rating, author, date, text, emotion))
		
		self.connection.commit()
						
							
		
