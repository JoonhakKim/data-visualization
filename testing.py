
import sqlite3

import sqlite3


name1= input("name of the db: ")

conn = sqlite3.connect(name1)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in DB:", tables)
print(type(tables))



name2 = input("name of the stock: ")

cursor.execute("SELECT * FROM AAPL WHERE Ticker = ?", (name2,))
info = cursor.fetchall()
print(info)
column_names = [description[0] for description in cursor.description]
print(column_names)



#print(info)

conn.close()
