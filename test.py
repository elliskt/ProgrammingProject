# import pandas as pd
# import numpy as np
# import matplotlib.pylab as plt

# d1 = {'id': ['ball', 'pending', 'pen'],
#       'brand': [11,22,33]}

# d2 = {'id': ['ball', 'ball', 'pen', 'ball'],
#       'color': ['rrr', 'rrr', 'bbb', 'ccc'],
#       'brand': [11,22,33, 44]}

# a = pd.DataFrame(d1)
# b = pd.DataFrame(d2)

# new = {'ball': 'fuck'}
# cata = ('a1','b2','c3')

# # price = {'ball':1, 'pen':2, 'asdf':3, 'ball': 4}
# # b['price'] = b['id'].map(price)
# group = b['brand'].grpby(b['id'])
# print (np.random.choice(cata, 100))

# plt.figure()
# data = {'s1':[20,30,40],
#         's2':[60,70,80],
#         's3':[10,20,30]}
# df = pd.DataFrame(data)
# x = np.arange(3)
# print(x)
# plt.plot(x, df)

# plt.legend(data)
# plt.show()

# # here is change

from db import *

db = database()
# records = db.getDB("Locations")
# records = db.getBikesInLocation(_location_id=3)
records = db.getColumnsInDB( "Bikes", "id, location_id")
for r in records:
	print(r)
# db.cursor.execute("""SELECT id, location_id FROM Bikes
# 	WHERE location_id = 1""")
# print(db.cursor.fetchall())
# db.printDB("Locations")
