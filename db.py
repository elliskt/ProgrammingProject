import sqlite3 as sql
import numpy as np
#import deprecated

class database(object):
    def __init__(self):
        self.db = sql.connect('bikesharing.db')
        self.cursor = self.db.cursor()
        self.db.execute("PRAGMA foreign_keys = 1") #Enable foreign key in SQLite3
        
    # ----------------------- user -----------------------------------
    def addUser(self, _mobile, _pswd, _name, _type):
        try:
            self.cursor.execute(""" INSERT INTO Users(mobile, pswd, balance, using_bikeid)
                VALUES({}, {}, 10, NULL)""".format(_mobile, _pswd,))
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
        self.cursor.execute("""SELECT * FROM Users WHERE mobile = ? AND pswd = ?""", (mobile, pswd))
        if count == 1:
            bike_id = self.cursor.fetchall()[0][3]
            return "USER_VERIFIED", bike_id
        else:
            self.cursor.execute("""SELECT COUNT(1) FROM Users WHERE mobile = ?""", (mobile,))
            count = self.cursor.fetchall()[0][0]
            if count == 1:
                return "USER_NOT_VERIFIED", ""
            else:
                return "USER_NOT_EXIST", ""

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

    def getColumnsInDB(self, data):
        try:
            table, columns = data[0], data[1]
            self.cursor.execute((" SELECT name,id FROM "+table))
            return self.cursor.fetchall()
        except sql.OperationalError as e:
            return e

    def getBikesInLocation(self, location_id):
        self.cursor.execute((" SELECT * FROM Bikes WHERE location_id={} AND in_use = 'False' ".format(str(location_id))))
        return self.cursor.fetchall()
    
    def getBikeLocation(self, bid):
        try:
            self.cursor.execute((" SELECT location_id FROM Bikes WHERE id={} ".format(str(bid))))
            loc = self.cursor.fetchall()
            return loc[0][0]
        except sql.OperationalError as e:
            return e


    def payBill(self, mobile, bike_id, duration, bill, start_location_id, return_location_id, date):
        # -------- get balance ---
        self.cursor.execute(("SELECT * FROM Users WHERE mobile = '{}'".format(mobile)))
        balance = self.cursor.fetchall()[0][2]
        balance -= bill
        # ------- update balance ---
        self.cursor.execute(("UPDATE Users SET balance={} WHERE mobile='{}'".format(balance, mobile)))
        self.db.commit()
        print("[Server] {} paid £ {}.".format(mobile, bill))
        # -------- logging --------
        self.recordLog(mobile, bike_id, duration, bill, start_location_id, return_location_id, date)
        print("[Server] {} 's trip has been logged.".format(mobile))
        return balance
    # ----- Insert log info -----
    def recordLog(self, mobile, bike_id, duration, bill, start_location_id, return_location_id, date):
        id = self.countLog()+1
        self.cursor.execute("INSERT INTO Log(id, mobile, bike_id, cost, duration, start_location_id, return_location_id, date) VALUES(?,?,?,?,?,?,?,?)",
                            (id, mobile, bike_id, bill, duration, start_location_id, return_location_id, date))
        self.db.commit()
        
    def countLog(self):
        self.cursor.execute("SELECT COUNT(*) FROM Log")
        count = self.cursor.fetchall()
        return int(count[0][0])
    
    def countLogperStation(self,date):
        today = date[0].replace('-','/',2)
        try:
            self.cursor.execute("""SELECT COUNT(*) FROM (
                                SELECT * FROM Log
                                WHERE date ='{}' AND start_location_id = {}
                                ) ;""".format(today,date[1]))
            count = self.cursor.fetchall()
            print(count)
            if not count:
                return 0
            else:
                return count[0][0]
        except sql.OperationalError as e:
            return e
    
    def getIncomeperStation(self):
        try:
            self.cursor.execute("SELECT SUM(cost) FROM Log GROUP BY start_location_id;")
            Income = self.cursor.fetchall()
            #"detuple" the tuples in the list using list comprehension
            return [i for t in Income for i in t]
        except sql.OperationalError as e:
            return e
        
    def getBrokenbikesperStation(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Bikes WHERE reported = 'True' GROUP BY location_id;")
            badBikes = self.cursor.fetchall()
            #"detuple" the tuples in the list using list comprehension
            return [i for t in badBikes for i in t]
        except sql.OperationalError as e:
            return e

    def writeReport(self, data):
        # (bike_id, user_id, location_id, error_type, date)
        self.cursor.execute("INSERT INTO Bikes_report(bike_id, user_id, location_id, error_type, date) VALUES(?,?,?,?,?)",
                            (data[0], data[1], data[2], data[3], data[4]))
        self.cursor.execute("UPDATE Bikes SET reported='{}' WHERE id={}".format(str('True'), str(data[0])))
        self.db.commit()
        print("[Server] {} reported the Bike-{}.".format(data[1], data[0]))
        print("[Server] Bike-{} reported status ---> True.".format(data[0]))

    def getAllBikes(self):
        self.cursor.execute("SELECT * FROM Bikes")
        return self.cursor.fetchall()

    def moveBike(self, data):
        self.cursor.execute("UPDATE Bikes SET location_id={} WHERE id={}".format(str(data[1].split('-')[0]), str(data[0])))
        self.db.commit()

    def fixBike(self, data):
        self.cursor.execute(
            "UPDATE Bikes SET reported='{}' WHERE id={}".format('False', str(data[0])))
        self.db.commit()

    def rentBike(self, data):
        self.cursor.execute(
            "UPDATE Bikes SET in_use='True' WHERE id={}".format(str(data[0])))
        self.cursor.execute(
            "UPDATE Bikes SET time_from='{}' WHERE id={}".format(str(data[1]), str(data[0])))
        self.cursor.execute(
            "UPDATE Users SET using_bikeid={} WHERE mobile='{}'".format(data[0], str(data[2])))
        self.db.commit()

    def sendLocation(self,data):
        self.cursor.execute(
            "UPDATE Bikes SET loc_latitude={} WHERE id={}".format(str(data[1]), str(data[0])))
        self.cursor.execute(
            "UPDATE Bikes SET loc_longtitude={} WHERE id={}".format(str(data[2]), str(data[0])))
        self.db.commit()

    def returnBikeReset(self, data):
        print("[Server] Bike-{} has been returned.".format(data[0]))
        self.cursor.execute(
            "UPDATE Bikes SET time_from=NULL WHERE id={}".format(str(data[0])))
        self.cursor.execute(
            "UPDATE Bikes SET loc_latitude=NULL WHERE id={}".format(str(data[0])))
        self.cursor.execute(
            "UPDATE Bikes SET loc_longtitude=NULL WHERE id={}".format(str(data[0])))
        self.cursor.execute(
            "UPDATE Bikes SET in_use='False' WHERE id={}".format(str(data[0])))
        self.cursor.execute(
            "UPDATE Bikes SET location_id={} WHERE id={}".format(str(data[1]), str(data[0])))
        self.cursor.execute(
            "UPDATE Users SET using_bikeid=NULL WHERE mobile='{}'".format(str(data[2])))
        self.db.commit()

    def calDuration(self, data):
        self.cursor.execute("SELECT time_from FROM Bikes WHERE id={}".format(data[0]))
        time = self.cursor.fetchall()[0][0]
        return time