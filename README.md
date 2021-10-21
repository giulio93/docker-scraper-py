# docker-scraper-py
A simple docker container that runs a cron job daily to scrape the table present in [https://www.enforcementtracker.com] and populate a sqlite database.

## How it works
The cron job invokes a daily shell script that triggers the python script. The python script uses the request library to get the data in json format. Each element of the json data array contains one row of the table, plus all the information under the "plus" widget attached to each row. The data is used to populate the table database. The python time library is used to add the current timestap to the GET request. Each row is stored in a sqlite database, which can be queried using the queries.py script. Scraping is incremental, only new rows (not already saved in the database) will be added every day!

## How to install and use it
Copy the repository and build from the Dockerimage:


`$ sudo docker build --rm -t docker-scraper . `


Run the docker container and access with a bash interface:
```bash
$ sudo docker exec -t -i $(sudo docker run -t -i -d docker-scraper) /bin/bash
```


Check if the cron job is running properly: once connected to the container use the tail -f command to see the cron log output. (Wait until you see any output)

```bash
$root@5ed72d77c714:/app# tail -f /var/log/cron.log
Tue Oct 19 13:53:01 UTC 2021: Scraper started!
ETid-1 has been added!
ETid-2 has been added!
ETid-3 has been added!
ETid-4 has been added!
[..]
ETid-875 has been added!
ETid-876 has been added!
The database has added : 876 new rows
The database has: [876] rows in total

```

The scraper job is running and the database is populated. 
Now let's query the database! 


## Quering the database
Exit from the tail -f output (CTRL + D) and query the database using the custom command!
Use the help function to show which queries are available:
```bash
root@5ed72d77c714:/app# python3 queries.py help
   
```

For example:

* The number of penalties for a specific country
* The average of fine given a specific country
```bash
root@d1c64cda7448:/app# python3 queries.py italy
The number of penalties gathered by italy is 96
The avarage fine for italy is 59.583333333333336
   
```
The number of penalties loaded in the database between two dates (based
on date of decision field)

```bash
root@d1c64cda7448:/app# python3 queries.py 2020-01-01 2021-01-01
The number of penalties present in the database between 2020-01-01 AND 2021-01-01 is: 358
   
```



