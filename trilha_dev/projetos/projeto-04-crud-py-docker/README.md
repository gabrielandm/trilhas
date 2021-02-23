# Introduction 
This is a REST API made to make all the CRUD functions to a AzureSQL database that has products stored. And the idea is that the user will be able to use the API from anywhere, so the API needs to get deployed into AKS as requested. To do that a Dockerfile was added and the project was uploaded to a repository inside DevOps.

# Requirements
To run the API without deploying to AKS you will only need to install the following python packages and the pyodbc driver 17.
- sqlalchemy
- Flask
- pyodbc
Don't forget to import urllib too.

# Getting Started
To test the API without beeing deployed you only need Flask.
1.	Create a database, I used Azure's database.
2.	Connect the project to the python API.
3.	Create a cluster using AKS.
4.	Upload the project to a repository (can be a GitHub repository too).
5.  Go to the Deployment center found inside the cluster and use the repository you created.
6.  Wait for the container be created using the Dockerfile you created.
7.  Test the API using your browser :) 

## Important things to remember
1.  The right port needs to be configured either in the code and in AKS, by default you will be using port 80, so don't forget to change the code or in AKS.
2.  Don't forget to install all the dependecies needed to run the API.
> Use Python 3.9.1 image
> Install Unix ODBC and PyODBC
> Install all the 3 packages