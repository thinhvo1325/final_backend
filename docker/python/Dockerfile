#===============================================
#======  Using Python 3.9 build Imange =========
#===============================================

# pull official base image
FROM python:3.12.6-bullseye

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./api/app /api/app

RUN pip install -r /api/app/requirements.txt

RUN apt-get install supervisor -y

# COPY ./api/app/supervisor/config/update_result.conf /etc/supervisor/conf.d/update_result.conf
# copy project

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /app/workers/logs

EXPOSE 8000
