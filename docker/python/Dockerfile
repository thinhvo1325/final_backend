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


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y


RUN pip install -r /api/requirements.txt

# copy project
COPY ./api/app /api/app

EXPOSE 8000
