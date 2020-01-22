# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.0-alpine

# Set enviroment variables - Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install pillow dependencies
RUN apk --no-cache add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev \
        tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

# create root directory for our project in the container
RUN mkdir /inventory_api

# Set the working directory
WORKDIR /inventory_api

# Copy the current directory contents into the container at /inventory_api
ADD . /inventory_api

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt