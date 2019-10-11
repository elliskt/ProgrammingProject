import sqlite3 as sql
import numpy as np

with sql.connect("bikesharing.db") as db:
	db.execute("PRAGMA foreign_keys = 1") #Enable foreign key in SQLite3
	cursor = db.cursor()

def printDB(table):
	print(table, "table: ")
	cursor.execute(""" SELECT * FROM {}""".format(table))
	for i in cursor.fetchall():
		print(i)

def addUsers():
	users = ['Mohammad', 'Razvan', 'Yihao', 'Ellis', 'Hafsah']
	for i in range(len(users)):
		addUser(i, np.random.randint(0, 100), users[i], 1)
	
def addLocations():
	locations = ['UofG', 'Strathclyde', 'Caledonian']
	for i in range(len(locations)):
		addLocation(i, locations[i])

def addBikes():
	for i in range(11):
		addBike(i, np.random.randint(0, 4))

#==================== USERS ====================
#User Types: Client = 1, Manager = 2, Operator = 3
cursor.execute(""" CREATE TABLE IF NOT EXISTS Users(
	mobile	TEXT PRIMARY KEY,
	pswd	TEXT NOT NULL,
	name	TEXT NOT NULL,
	type	INTEGER NOT NULL
);""")
db.commit()

def addUser(_mobile, _pswd, _name, _type):
	try:
		cursor.execute(""" INSERT INTO Users(mobile, pswd, name, type)
			VALUES(?, ?, ?, ?);""", (_mobile, _pswd, _name, _type))
		db.commit()
	except sql.IntegrityError as e:
		if e.args[0] == 'UNIQUE constraint failed':
			print("ERROR: User mobile exists")
		else:
			print("ERROR: ", e.args[0])

def deleteUser(_mobile):
	cursor.execute("DELETE FROM Users WHERE mobile='{}';".format(_mobile))
	db.commit()


#==================== BIKES ====================
cursor.execute(""" CREATE TABLE IF NOT EXISTS Bikes(
	id 			INTEGER PRIMARY KEY,
	location_id	INTEGER,
	condition 	BOOLEAN,
	FOREIGN KEY (location_id) 
		REFERENCES Locations(id)
);""")
db.commit()

def addBike(_id, _location_id):
	try:
		cursor.execute(""" INSERT INTO Bikes(id, location_id, condition)
			VALUES(?, ?, ?);""", (_id, _location_id, True))
		db.commit()
	except sql.IntegrityError as e:
		if e.args[0] == 'FOREIGN KEY constraint failed':
			print("ERROR: Location does not exist")
		elif e.args[0] == 'UNIQUE constraint failed':
			print("ERROR: Bike ID exists")
		else:
			print("ERROR: ", e.args[0])

def deleteBike(_id):
	cursor.execute("DELETE FROM Bikes WHERE id={};".format(_id))
	db.commit()

def changeBikeCondition(_id, _condition):
	cursor.execute("UPDATE Bikes SET condition=? WHERE id=?;", (_condition, _id))
	db.commit()

def changeBikeLocation (_id, _location_id):
	cursor.execute("UPDATE Bikes SET location_id=? WHERE id=?;", (_location_id, _id))
	db.commit()

#==================== LOCATIONS ====================
cursor.execute(""" CREATE TABLE IF NOT EXISTS Locations(
	id		INTEGER PRIMARY KEY,
	name	TEXT
);""")
db.commit()

def addLocation(_id, _name):
	try:
		cursor.execute("INSERT INTO Locations (id,name) VALUES (?, ?);",
			(_id, _name))
		db.commit()
	except sql.IntegrityError as e:
		print("ERROR: ", e.args[0])

def deleteLocation(_id):
	cursor.execute("DELETE FROM Locations WHERE id=?;", (_id))
	db.commit()


#==================== LOG ====================
cursor.execute(""" CREATE TABLE IF NOT EXISTS Log(
	mobile INTEGER,
	bike_id INTEGER,
	cost INTEGER,
	condition TEXT,
	start_time TIME,
	end_time TIME,
	FOREIGN KEY (bike_id) 
		REFERENCES Bikes(id),
	FOREIGN KEY (mobile) 
		REFERENCES Users(mobile)
);""")


#=================== TESTING ===================
# addUsers()
# addLocations()
# addBikes()
printDB("Users")
printDB("Locations")
printDB("Bikes")
db.close()

