# docker-scraper-py
A simple docker container that runs a cron invoking a shell script.
The script scrape [https://www.enforcementtracker.com] and populate a sqlite database.

## How it works
A cron job trigger a python script daily.
The python script user request library in order to get the data in json format. The same data that are used to populate each row of the table in the side, and also the info under the plus button widget attached to each row.
The request need the current time stamp, that is provided by the python time library.
Each row is saved in a sqlite database, that can be queried later.
The scraping is incremental, only new lines will be added every day

## How to install and use it
Copy the repository and build from the Dockerimage:


`$ sudo docker build --rm -t docker-scraper . `


Run the docker container and access with a bash interface:
```bash
$ sudo docker exec -t -i $(sudo docker run -t -i -d docker-scraper) /bin/bash
```


Check if it is running properly, once connected to the container, viewing the logfile. (Wait until you see any output)

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



