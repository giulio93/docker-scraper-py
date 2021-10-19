#!/bin/sh
echo "$(date): executed script" >> /var/log/cron.log 2>&1
python3 /app/hello.py >> /var/log/cron.log 2>&1
python3 /app/main.py >> /var/log/cron.log 2>&1
