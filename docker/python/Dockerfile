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

# copy project

EXPOSE 8000
