import sqlite3
import sys

con = sqlite3.connect('/app/scraped_database.db')
con.row_factory = lambda cursor, row: row[0]
cur = con.cursor()

def help():
    print("""

 /$$$$$$$                      /$$                                  /$$$$$$                                                            
| $$__  $$                    | $$                                 /$$__  $$                                                           
| $$  \ $$  /$$$$$$   /$$$$$$$| $$   /$$  /$$$$$$   /$$$$$$       | $$  \__/  /$$$$$$$  /$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
| $$  | $$ /$$__  $$ /$$_____/| $$  /$$/ /$$__  $$ /$$__  $$      |  $$$$$$  /$$_____/ /$$__  $$|____  $$ /$$__  $$ /$$__  $$ /$$__  $$
| $$  | $$| $$  \ $$| $$      | $$$$$$/ | $$$$$$$$| $$  \__/       \____  $$| $$      | $$  \__/ /$$$$$$$| $$  \ $$| $$$$$$$$| $$  \__/
| $$  | $$| $$  | $$| $$      | $$_  $$ | $$_____/| $$             /$$  \ $$| $$      | $$      /$$__  $$| $$  | $$| $$_____/| $$      
| $$$$$$$/|  $$$$$$/|  $$$$$$$| $$ \  $$|  $$$$$$$| $$            |  $$$$$$/|  $$$$$$$| $$     |  $$$$$$$| $$$$$$$/|  $$$$$$$| $$      
|_______/  \______/  \_______/|__/  \__/ \_______/|__/             \______/  \_______/|__/      \_______/| $$____/  \_______/|__/      
                                                                                                         | $$                          
                                                                                                         | $$                          
                                                                                                         |__/                                                                                                                                                                                                                            
            """)
    print("The number of penalties for a specific country  ==> python3 queries.py <country_name>")
    print("The average of fine given a specific country    ==> python3 queries.py <country_name>")
    print("Please select one of the country in the list:")
    cur.execute('SELECT DISTINCT(Country) FROM penalties')
    print(cur.fetchall())
    print("=====================================================================================")
    print("The number of penalties loaded in the database between two dates  ==> python3 queries.py <date_from> <date_to>")
    print("!!!!!! PLEASE INPUT DATE IN THIS FORMAT YYYY-MM-DD !!!!!")    



if(len(sys.argv)==2):
    if(str(sys.argv[1])=="help"):
        help()    
    else:
            #The number of penalties for a specific country 
            cur.execute('SELECT COUNT(ETid) FROM penalties WHERE Country="'+sys.argv[1].upper()+'"')
            pen_for_c = cur.fetchall()
            #The average of fine given a specific country 
            cur.execute('SELECT AVG(Fine) FROM penalties WHERE Country="'+sys.argv[1].upper()+'"')
            avg_fine_per_c = cur.fetchall()
            if(pen_for_c[0]==0 and avg_fine_per_c[0]==None):
                help()
            else:
                print("The number of penalties gathered by "+sys.argv[1]+" is "+str(pen_for_c[0]))
                print("The avarage fine for "+sys.argv[1]+" is "+str(avg_fine_per_c[0]))
elif(len(sys.argv)==3):
    #The number of penalties loaded in the database between two dates (based on date of decision field) 
    cur.execute('SELECT COUNT(ETid) FROM penalties WHERE Date BETWEEN "'+str(sys.argv[1])+'" AND "'+str(sys.argv[2])+'"')
    count_per_data=cur.fetchall()
    print(count_per_data)
    if(count_per_data[0]==0):
        print("No penalties present in the range presented")
    else:
        print("The number of penalties present in the database between "+str(sys.argv[1])+" AND "+str(sys.argv[2])+" is: " + str(count_per_data[0]))
else: help()