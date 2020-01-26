# Inventory API

## System Requirements

You need **Docker Engine** and **Docker Compose**. Install it from [Docker Website](https://docs.docker.com/)

## Python Environment Setup

Create a **.env** file inside **inventory_api** directory. We are using [python-decouple](https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html) library for handling environment variables.


## Build the Services

    $ docker-compose build


## Starting App
    $ docker-compose up

Access it through **http://0.0.0.0:8000**

## Documentation

### API Endpoints

Registration Endpoint: /api/v1/accounts/register/

Login Endpoint: /api/v1/accounts/login/

Logout Endpoint: /api/v1/accounts/logout/

Category Endpoints: /api/v1/catalogue/category/

Product Endpoints: /api/v1/catalogue/product/

Request Product Endpoints: /api/v1/catalogue/request-item/

Issue Product Endpoints: /api/v1/catalogue/request-item/<int:pk>/issue-item/

### Role Based Perms

Category Endpoints - Admin has full access or non-staff users can have read-only access

Product Endpoints - Admin has full access or non-staff users can have read-only access

Request Product Endpoints - Admin has read-only access or non-staff users can have full access

Issue Product Endpoints - Admin has full access or non-staff users can have read-only access

## Code Styling

Before code pushing, run [flake8](https://simpleisbetterthancomplex.com/packages/2016/08/05/flake8.html) for code styling and [isort](https://simpleisbetterthancomplex.com/packages/2016/10/08/isort.html) for organizing the imports.

    $ docker-compose run web flake8
    $ docker-compose run web isort -rc .
