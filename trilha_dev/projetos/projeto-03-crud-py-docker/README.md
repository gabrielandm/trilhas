# CRUD with Python using containers (Docker Desktop)

The idea of this project is to try to run the [last project](../projeto-02-crud-py/projeto-02-crud-py.py) using containers in a local machine.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The first thing you'll need is [Docket Desktop](https://www.docker.com/products/docker-desktop).

### How to set a Dockerfile

Dockerfile is a crucial part of this project without it you can't configure your image to make the container work correctly. So let's go step by step in the creation of a Dockerfile just like [this one](Dockerfile)...

1 - You start by creating a file named Dockerfile without extensions.

2 - Choose a template image [here](https://hub.docker.com) to start your conatiner. I reccomend you to use [python's](https://hub.docker.com/_/python) officail image so you already have Python installed on it. After choosing a image you'll need to choose a version for your python image like this:

> FROM python:\<your Python version\>

3 - Now you will need to install [UnixODBC](http://www.unixodbc.org) on your image by running a couple of commands, you only need to type the RUN command on the Dockerfile like this:

> RUN apt-get update && apt-get install -y --no-install-recommends \\ \
>    unixodbc-dev \\ \
>    unixodbc \\ \
>    libpq-dev 

4 - Know that you installed the UnixODBC you can install [ODBC Driver 17 from MS Documentation for Debian](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15) and use this commands:

>RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \\ \
>    curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \\ \
>    apt-get update && \\ \
>    ACCEPT_EULA=Y apt-get install msodbcsql17 && \\ \
>    ACCEPT_EULA=Y apt-get install mssql-tools && \\ \
>    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile && \\ \
>    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \\ \
>    apt-get install -y unixodbc-dev

5 - Install all the packages needed to run the .py file:

> RUN pip install sqlalchemy Flask pyodbc

6 - Copy you .py file to the container:

> COPY projeto-03-crud-py-docker.py .

7 - Run the .py file to start the web service:

> CMD [ "python", "./projeto-03-crud-py-docker.py" ]

know you are done installing the Dockerfile.

## Running the tests

To run the tests it's very simple, use cd command to go to the Dockerfile directory and to run the following commands (don't forget to run Docker Desktop on your machine):

> docker build -t [image's name] .

Know Docker built the image and you can create a container using that same image...

> docker run -d -p 80:80 --name [container's name] [image's name]

After this command Docker will start to run your image and create a web service on a container inside you machine. You can test the web service via [Insomnia](https://insomnia.rest/download), [Postman](https://www.postman.com/downloads/) or even your browser if the method is set to GET.


### Problems you might encounter

1 - A common problem that can appear to you while trying to run this .py file is that sometimes Flask get installed using production mode... this may be a problem if Flask warns you saying that it can only run using development mode, you can check use the following command after installing Flask package in your image:

> ENV FLASK_ENV=development

2 - Configure your flask python file to use port 80

## Author

* **Gabriel M De Paoli** - [*github*](github.com/gabrielpaoli-dev)
