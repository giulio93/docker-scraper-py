FROM ubuntu:18.04

# Install cron
RUN apt-get install -y apt-transport-https &&  apt-get update 
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install cron

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/simple-cron

# Add shell script and grant execution rights
ADD script.sh /script.sh
RUN chmod +x /script.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

COPY requirements.txt ./

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY main.py /app/main.py
COPY queries.py /app/queries.py


# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
