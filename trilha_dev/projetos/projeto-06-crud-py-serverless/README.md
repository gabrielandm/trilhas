# CRUD with NodeJs

This project was made to test some skills using Node, Azure Functions and Azure's Database by making an Api that makes a full CRUD to a database (Azure SQL).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The first thing you'll need is [Python 3](https://www.python.org/downloads/) to be installed on your machine so you can use python commands and run your code.

For testing I recommend using [VS Code](https://code.visualstudio.com/download) because it has some features that will be used in this README.

### Installing

1 - Run pip install command:

> python -m pip install -r requirements.txt

2 - Install [Azure Function extension](Https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) to your VS Code.

```
id: ms-azuretools.vscode-azurefunctions
```

If the installation was successful you'll have a new icon added to the left of your VS Code.

## Running the tests

To run the tests is very simple, since we have Azure Funtion's extension installed we can simply run the following command:

> func start

After this command the extension will start your functions and you can test all functions via [Insomnia](https://insomnia.rest/download), [Postman](https://www.postman.com/downloads/) or even your browser if the method configured in your function.json ([example](productSearchFiltered/function.json))

## Deployment

To deploy this functions using VS Code you can follow the [official Microsoft guide for Azure Function's extenion](https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=csharp)

## Author

* **Gabriel M De Paoli** - [*github*](github.com/gabrielpaoli-dev)
