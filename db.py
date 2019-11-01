import sqlite3 as sql
import numpy as np
#import deprecated

class database(object):
	def __init__(self):
		self.db = sql.connect('bikesharing.db')
		self.cursor = self.db.cursor()
		self.db.execute("PRAGMA foreign_keys = 1") #Enable foreign key in SQLite3

		# Initializing DBs

		#User Types: Client = 1, Manager = 2, Operator = 3
		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Users(
			mobile	TEXT PRIMARY KEY,
			pswd	TEXT NOT NULL,
			name	TEXT,
			type	INTEGER NOT NULL
		);""")
		self.db.commit()

		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Bikes(
			id 			INTEGER PRIMARY KEY,
			location_id	INTEGER,
			condition 	BOOLEAN,
			FOREIGN KEY (location_id) 
				REFERENCES Locations(id)
		);""")
		self.db.commit()

		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Locations(
			id		INTEGER PRIMARY KEY,
			name	TEXT
		);""")
		self.db.commit()

		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Log(
			mobile		INTEGER,
			bike_id		INTEGER,
			cost		INTEGER,
			condition	TEXT,
			start_time	TIME,
			end_time	TIME,
			FOREIGN KEY (bike_id) 
				REFERENCES Bikes(id),
			FOREIGN KEY (mobile) 
				REFERENCES Users(mobile)
		);""")
		self.db.commit()

	#==================== USERS ====================
	def addUser(self, _mobile, _pswd, _name, _type):
		try:
			self.cursor.execute(""" INSERT INTO Users(mobile, pswd, name, type)
				VALUES(?, ?, ?, ?);""", (_mobile, _pswd, _name, _type))
			self.db.commit()
		except sql.IntegrityError as e:
			if e.args[0] == 'UNIQUE constraint failed: Users.mobile':
				return "USER_EXISTS" # User exists
			else:
				print("ERROR: ", e.args[0])
		return "USER_REGISTERD" # Operation successful

	def verifyUser(self, mobile, pswd):  # return
		self.cursor.execute("""SELECT COUNT(1) FROM Users WHERE mobile = ? AND pswd = ?""", (mobile, pswd))
		count = self.cursor.fetchall()[0][0] 
		if count == 1:
		    return "USER_VERIFIED"
		else:
			self.cursor.execute("""SELECT COUNT(1) FROM Users WHERE mobile = ?""", (mobile,))
			count = self.cursor.fetchall()[0][0]
			if count == 1:
			    return "USER_NOT_VERIFIED"
			else:
				return "USER_NOT_EXIST"

	def deleteUser(self, _mobile):
		self.cursor.execute("DELETE FROM Users WHERE mobile='{}';".format(_mobile))
		self.db.commit()


	#==================== BIKES ====================
	def addBike(self, _id, _location_id):
		try:
			self.cursor.execute(""" INSERT INTO Bikes(id, location_id, condition)
				VALUES(?, ?, ?);""", (_id, _location_id, True))
			self.db.commit()
		except sql.IntegrityError as e:
			if e.args[0] == 'FOREIGN KEY constraint failed':
				print("ERROR: Location does not exist")
			elif e.args[0] == 'UNIQUE constraint failed: Bikes.id':
				print("ERROR: Bike ID exists")
			else:
				print("ERROR: ", e.args[0])

	def deleteBike(self, _id):
		self.cursor.execute("DELETE FROM Bikes WHERE id={};".format(_id))
		self.db.commit()

	def changeBikeCondition(self, _id, _condition):
		self.cursor.execute("UPDATE Bikes SET condition=? WHERE id=?;", (_condition, _id))
		self.db.commit()

	def changeBikeLocation (self, _id, _location_id):
		self.cursor.execute("UPDATE Bikes SET location_id=? WHERE id=?;", (_location_id, _id))
		self.db.commit()

	#==================== LOCATIONS ====================
	def addLocation(self, _id, _name):
		try:
			self.cursor.execute("INSERT INTO Locations (id,name) VALUES (?, ?);",
				(_id, _name))
			self.db.commit()
		except sql.IntegrityError as e:
			if e.args[0] == "UNIQUE constraint failed: Locations.id":
				print("ERROR: Location ID exists")

	def deleteLocation(self, _id):
		self.cursor.execute("DELETE FROM Locations WHERE id=?;", (_id))
		self.db.commit()


	#==================== LOG ====================
	#================== GENERAL ==================
	def printDB(self, table):
		print(table, "table: ")
		self.cursor.execute(""" SELECT * FROM {}""".format(table))
		for i in self.cursor.fetchall():
			print(i)

	# Deprecated 
	def getDB(self, table):
		try:
			self.cursor.execute(""" SELECT * FROM {}""".format(table))
			return self.cursor.fetchall() #returns a list of DB records
		except sql.OperationalError as e:
			return e

	# Deprecated
	def getBikesInLocation(self, _location_id):
		try:
			self.cursor.execute(""" SELECT id FROM Bikes
				WHERE location_id = {}""".format(_location_id))
			return self.cursor.fetchall()
		except sql.OperationalError as e:
			print("Location does not exist!")

	def getColumnsInDB(self, data):
		try:
			table, columns = data[0], data[1]
			# print(data)
			# print((" SELECT "+columns+" FROM "+table))
			self.cursor.execute((" SELECT "+columns+" FROM "+table))
			return self.cursor.fetchall()
		except sql.OperationalError as e:
			return e



#=================== TESTING ===================
# Uncomment and run file to repopulate DB
	#=============== INITIAL DATA ================
	# def addUsers(self):
	# 	self.users = ['Mohammad', 'Razvan', 'Yihao', 'Ellis', 'Hafsah']
	# 	for i in range(len(self.users)):
	# 		self.addUser(i, i, self.users[i], 1)
		
	# def addLocations(self):
	# 	self.locations = ['UofG', 'Strathclyde', 'Caledonian']
	# 	for i in range(len(self.locations)):
	# 		self.addLocation(i, self.locations[i])

	# def addBikes(self):
	# 	for i in range(10):
	# 		self.addBike(i, np.random.randint(0, 3))
# if __name__ == '__main__':
# 	db = database()
# 	db.addUsers()
# 	db.addLocations()
# 	db.addBikes()
# 	db.printDB("Users")
# 	db.printDB("Locations")
# 	db.printDB("Bikes")
# db.close()

