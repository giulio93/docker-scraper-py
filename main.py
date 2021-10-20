import requests
import sqlite3
import json
import time
from datetime import datetime
import re



#Function that will populate the database
def populate(cur,today_timestamp):
    #Try to create the penalties table,if not exist already
    ETids = []
    new_rows_count = 0
    
    try:
        cur.execute('''CREATE TABLE penalties (ETid text, Country text, Date text, Fine real, Controller_Processor text,
                                               Quoted text,Type text,Source text,Autority text,Sector text,Summary text,Direct_url text)''')
    except sqlite3.OperationalError:
        ETids = cur.execute("SELECT ETid FROM penalties").fetchall()
        #print(ETid)
        #print("Table penalties already exists")
    #Get the json data directly from the XHR response
    r = requests.get('https://www.enforcementtracker.com/data.json?_='+str(today_timestamp)+'')
    data=r.json()
    #Fetch each raw in the payload
  
    for item in data["data"]:
        if(item[1] not in ETids):
            print(item[1]+" has been added!")
            new_rows_count+=1
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

            match = re.search(r'href=[\'"]?([^\'" >]+)', item[11])
            if match:
                link = match.group(1)
            else: link =" "
            #Scrape the Direct Url data
            match = re.search(r'href=[\'"]?([^\'" >]+)', item[12])
            if match:
                direct_url = match.group(1)         
            else: direct_url=" "
            #Insert the row inside the database
            cur.execute("INSERT INTO penalties  VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                                                        (item[1],item[2].split("/>",1)[1],ntime.date(),
                                                        item[5],item[6],item[8],item[9],link,item[3],
                                                        item[7],item[10],direct_url))
            con.commit()
    return new_rows_count
#Connect to the Database and populate and call the populate function
con = sqlite3.connect('/app/scraped_database.db')
con.row_factory = lambda cursor, row: row[0]
cur = con.cursor()
new_rows_count = populate(cur,time.time())


cur.execute("SELECT COUNT(ETid) FROM penalties")
print("The database has added : "+str(new_rows_count)+" new rows")
print("The database has: "+ str(cur.fetchall())+" rows in total")



