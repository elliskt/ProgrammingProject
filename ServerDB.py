import sqlite3


class DBFun(object):
    def __init__(self):
        self.db = sqlite3.connect('SharingBike.db')
        self.cursor = self.db.cursor()
        self.customer = None
        self.bike = None
        self.bikestop = None

    def verify_un_pw(self, un, pw):
        if self.check_registered(un) == False:          # check the username existence
            return "USER_NOT_EXIST"
        else:
            self.cursor.execute("SELECT COUNT(1) FROM Customer WHERE username = ? and password = ?", (un, pw))      # check the username and password
            if self.cursor.fetchall()[0][0] == 0:
                return "USER_UNVERIFIED"
            else:
                return "USER_VERIFIED"

    def client_register(self, un, pw):
        if self.check_registered(un):
            return 'USER_ALREADY_EXIST'
        else:
            # save to database
            self.cursor.execute("""INSERT INTO Customer(username,password, balance) VALUES(?,?,?)""", (un, pw, 0))
            self.db.commit()
            return 'USER_REGISTERED'

    def check_registered(self, un):  # return
        self.cursor.execute("""SELECT COUNT(1) FROM Customer WHERE username = ?""", (un,))
        if self.cursor.fetchall()[0][0] == 1:
            return True
        else:
            return False

    # def create_table(self):
    #     self.cursor.execute("""CREATE TABLE IF NOT EXISTS students(
    #     id integer PRIMARY KEY,
    #     name text NOT NULL,
    #     class text NOT NULL,
    #     grade integer);""")
    #     self.db.commit()
    #     self.db.close()


