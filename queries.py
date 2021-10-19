import sqlite3

con = sqlite3.connect('scraped_database.db')
cur = con.cursor()
#The number of penalties loaded in the database between two dates (based on date of decision field) 
cur.execute('SELECT COUNT(Date) FROM penalties WHERE Date BETWEEN "2021-09-29" AND "2021-10-13"')
print(cur.fetchall())
#The number of penalties for a specific country 
cur.execute('SELECT COUNT(ETid) FROM penalties WHERE Country="SPAIN"')
print(cur.fetchall())
#The average of fine given a specific country 
cur.execute('SELECT AVG(Fine) FROM penalties WHERE Country="SPAIN"')
print(cur.fetchall())