# CRUD with Python

This project was an exercise that you needed to make a full CRUD to a Azure SQL database using any Python ORM and you could do it locally.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The first thing you'll need is [Python 3](https://www.python.org/downloads/) to be installed on your machine so you can use pyhon commands and run your .py codes.

### Installing

1 - Run python's pip install command to install all the dependecies of the [code in this project](projeto-02-crud-py.py):

> python -m pip install Flask sqlalchemy pyodbc

1.1 [Flask](https://flask.palletsprojects.com/en/1.1.x/) is a package that you can use to run your functions trought determinate routes using decorators (setting the address and method for each function) above above each function.

1.2 [SQLAlchemy](https://docs.sqlalchemy.org/en/13/) is a package that is a ORM, so you don't need to make the CRUD using SQL commands.

1.3 [PyODBC](https://github.com/mkleehammer/pyodbc/wiki) is only necessary if you want to connect the software to a SQL Server database.

2 - Install [ODBC Driver 17](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15) on your computer (if you want to use SQL Server database).

## Running the tests

To run the tests is very simple, you only need to run this command:

> py projeto-02-crud-py.py

After this command Python and Flask will start to run your file and create a web service on your local machine. You can test them via [Insomnia](https://insomnia.rest/download), [Postman](https://www.postman.com/downloads/) or even your browser if the method is set to GET.


### A problem you might encounter

A common problem that can appear to you while trying to run this .py file is that sometimes Flask get installed using production mode... this may be a problem that Flask will warn you saying that it can only run using development mode, you can check [this documentation](https://flask.palletsprojects.com/en/master/server/) to solve it.

## Author

* **Gabriel M De Paoli** - [*github*](github.com/gabrielpaoli-dev)
