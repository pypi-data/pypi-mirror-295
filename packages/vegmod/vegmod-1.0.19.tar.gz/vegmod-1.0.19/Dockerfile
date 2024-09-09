FROM python:3.12.4-bookworm

USER root

RUN apt-get update && apt-get install -y cron vim

# Setup the crontab
COPY ./vegmod.crontab /etc/cron.d/vegmod.crontab
RUN chmod 0644 /etc/cron.d/vegmod.crontab
RUN crontab /etc/cron.d/vegmod.crontab

# Set the working directory
WORKDIR /app

# Copy the source code
COPY . /app

# Install the app using setup.py
RUN pip install -e .

# Run cron
CMD ["sh", "-c", "env >> /etc/environment && cron -f"]