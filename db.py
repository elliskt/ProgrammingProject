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
            type	INTEGER NOT NULL);""")
        self.db.commit()

        # ----------- Create Bikes table --------------
        self.cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS `Bikes`(
        `id`	INTEGER,
        `location_id`	INTEGER,
        `in_use`	BOOLEAN,
        `loc_latitude`	REAL,
        `loc_longtitude`	REAL,
        `time_from`	DATETIME,
        `condition`	BOOLEAN,
        PRIMARY KEY(`id`),
        FOREIGN KEY(`location_id`) REFERENCES `Locations`(`id`)
        );""")
        self.db.commit()

        # ----------- Create Locations(Bike stop location) table --------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS `Locations` (
        `id`    INTEGER,
        `name`    TEXT,
        `loc_latitude`    REAL,
        `loc_longtitude`    REAL,
        PRIMARY KEY(`id`)
        );""")
        self.db.commit()

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Log(
            id             INTEGER,
            mobile        INTEGER,
            bike_id        INTEGER,
            cost        INTEGER,
            condition    REAL,
            duration    DATETIME,
            start_location_id    INTEGER,
            return_location_id    INTEGER,
            PRIMARY KEY (id)
            FOREIGN KEY (bike_id) 
                REFERENCES Bikes(id),
            FOREIGN KEY (mobile) 
                REFERENCES Users(mobile)
            FOREIGN KEY (start_location_id) 
                REFERENCES Locations(id),
            FOREIGN KEY (return_location_id) 
                REFERENCES Users(mobile)
        );""")
        self.db.commit()
    # ===============================================================

    # ----------------------- user -----------------------------------
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
    # =================================================================================

    # --------------------- bikes -----------------------------------------------------
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
    # ========================================================================

    # --------------------------- Locations -----------------------------------
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
    # def getBikesInLocation(self, _location_id):
    # 	try:
    # 		self.cursor.execute(""" SELECT id FROM Bikes
    # 			WHERE location_id = {}""".format(_location_id))
    # 		return self.cursor.fetchall()
    # 	except sql.OperationalError as e:
    # 		print("Location does not exist!")

    def getColumnsInDB(self, data):
        try:
            table, columns = data[0], data[1]
            self.cursor.execute((" SELECT name,id FROM "+table))
            return self.cursor.fetchall()
        except sql.OperationalError as e:
            return e

    def getBikesInLocation(self, location_id):
        print(location_id)
        self.cursor.execute((" SELECT * FROM Bikes WHERE location_id = " + str(location_id)))
        return self.cursor.fetchall()

    def payBill(self, mobile, bill):
        # -------- get balance ---
        self.cursor.execute(("SELECT * FROM Users WHERE mobile = '{}'".format(str(mobile))))
        balance = self.cursor.fetchall()[0][2]
        balance -= bill
        # ------- update balance ---
        self.cursor.execute(("UPDATE Users SET balance={} WHERE mobile='{}'".format(balance, mobile)))
        self.db.commit()
        if balance <= 0:
            return balance
        else:
            return balance

    def recordLog(self,  id, mobile, bike_id, duration, bill, start_location_id, return_location_id):


    def writeReport(self, data):
        # (bike_id, user_id, location_id, error_type, date)
        self.cursor.execute("INSERT INTO Bike_report(bike_id, user, location_id, report_type, time) \
                            VALUES({},'{}',{},'{}',{})".format(data[0], data[1], data[2], data[3], data[4]))
        self.db.commit()
        print("[Server] {} reported the Bike-{}.".format(data[1], data[0]))
