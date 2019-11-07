import sqlite3


class DBFun(object):
    def __init__(self):
        self.db = sqlite3.connect('SharingBike.db')
        self.cursor = self.db.cursor()
        self.customer = None
        self.bike = None
        self.bikestop = None



