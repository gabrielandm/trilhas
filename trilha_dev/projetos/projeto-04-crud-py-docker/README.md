# Python Api using AKS 
This is a REST API made to make all the CRUD functions to a AzureSQL database that has products stored. And the idea is that the user will be able to use the API from anywhere, so the API needs to get deployed into AKS. To do that a Dockerfile was added and the project was uploaded to a repository inside DevOps.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In this project you'll need access to AKS so you can deploy the container on it. And don't forget to check [project 3's README.md](../projeto-03-crud-py-docker/README.md) to create a functional Dockerfile.

### How to use AKS

You can follow this links to help you:

* [AKS Intro](https://docs.microsoft.com/en-us/learn/modules/intro-to-azure-kubernetes-service/)
* [Deploy container using AKS](https://docs.microsoft.com/en-us/learn/modules/aks-deploy-container-app/)
* [Simple way to deploy using only Azure Portal and not the Azure's Shell](https://youtu.be/YR0To89LHzc)

Don't forget to send your python file to a repository so AKS can always update the container with the most recent version of your service.

## Running the tests

After learning how to use AKS and deploying the project using Azure Portal, Azure will start to run your image and create a conatiner with your web service. You can test the web service via [Insomnia](https://insomnia.rest/download), [Postman](https://www.postman.com/downloads/) or even your browser if the method is set to GET.

## Author

* **Gabriel M De Paoli** - [*github*](github.com/gabrielpaoli-dev)
