import requests
import sqlite3
import json
import time
from datetime import datetime

#Function that will populate the database
def populate(cur,today_timestamp):
    #Try to create the penalties table,if not exist already
    try:
        cur.execute('''CREATE TABLE penalties (ETid text, Country text, Date text, Fine real, Controller_Processor text,Quoted text,Type text,Source text)''')
    except sqlite3.OperationalError:
        print("Table penalties already exists")
    #Get the json data directly from the XHR response
    r = requests.get('https://www.enforcementtracker.com/data.json?_='+str(today_timestamp)+'')
    data=r.json()
    #Fetch each raw in the payload

    for item in data["data"]:
        #Format the date
        if(item[4]=="Unknown"):#When a date is unknown we put the lowest value possible
            ntime =  datetime.strptime("1800-01-01","%Y-%m-%d")
        else:
            try:
                ntime =  datetime.strptime(item[4],"%Y-%m-%d")
            except ValueError:
                try:
                 ntime =  datetime.strptime(item[4],"%Y-%m")
                except ValueError:
                 ntime =  datetime.strptime(item[4],"%Y")

        #Scrape the link from the htlm structure
        link=item[11]
        if link=="":
            link="no Link"
        else:
            link=link.split(" ")[2]
        #Insert the row inside the database
        cur.execute("INSERT INTO penalties  VALUES(?,?,?,?,?,?,?,?)",(item[1],item[2].split("/>",1)[1],ntime.date(),item[5],item[6],item[8],item[9],link))
        con.commit()
#Connect to the Database and populate and call the populate function
con = sqlite3.connect('scraped_database.db')
cur = con.cursor()
populate(cur,time.time())

cur.execute("SELECT COUNT(ETid) FROM penalties")
print("The database has scraped: "+ str(cur.fetchall()))


