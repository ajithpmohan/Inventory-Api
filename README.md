# Inventory API

## System Requirements

You need **Docker Engine** and **Docker Compose**. Install it from [Docker Website](https://docs.docker.com/)

## Python Environment Setup

Create a **.env** file inside **inventory_api** directory. We are using [python-decouple](https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html) library for handling environment variables.

## Starting App

    $ docker-compose up

Access it through **http://localhost:8000**

## Code Styling

Before code pushing, run [flake8](https://simpleisbetterthancomplex.com/packages/2016/08/05/flake8.html) for code styling and [isort](https://simpleisbetterthancomplex.com/packages/2016/10/08/isort.html) for organizing the imports.

    $ docker-compose run web flake8
    $ docker-compose run web isort -rc .
