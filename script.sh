#!/bin/sh
echo "$(date): Scraper started!" >> /var/log/cron.log 2>&1
python3 /app/main.py >> /var/log/cron.log 2>&1
