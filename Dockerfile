FROM python:3.8-slim

WORKDIR /home/app

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install project libraries
COPY requirements.txt /home/app/
RUN pip install -r requirements.txt

# copy project files
COPY . /home/app/

ENTRYPOINT ["/home/app/entrypoint.sh"]