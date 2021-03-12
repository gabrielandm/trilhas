# REST Api CRUD with .NET Core through Azure Functions

This project was made to test some skills using .NET Core, Azure Functions, VS Code and Azure SQL by making an Api that makes a full CRUD to a Azure database.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The first thing you'll need is [.NET Core](https://dotnet.microsoft.com/download) to be installed on your machine so you can use dotnet commands.

For testing I recommend using [VS Code](https://code.visualstudio.com/download) or [Visual Studio 2019](https://visualstudio.microsoft.com/downloads/) because it has features that will be used in this README.

Install [Azure Function extension](Https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) to your VS Code.

```
id: ms-azuretools.vscode-azurefunctions
```

### Installing

1 - Go to Azure Funcitons extension and begin a new project using .NET Core and create a HTTP Trigger function. Check the [official documentaion](https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=csharp) for more info.

2 - Copy the Models folder and the [ProductApi.cs](ProductApi.cs) to your new project

3 - Install all .NET apckages needed using the following command: 

> dotnet add package [name of the package]

## Running the tests

To run the tests is very simple, since we have Azure Funtion's extension installed we can simply run the following command:

> func start

After this command the extension will start your functions and you can test them using [Insomnia](https://insomnia.rest/download), [Postman](https://www.postman.com/downloads/) or even your browser if the method is set to GET.

## Deployment

To deploy this functions using VS Code you can follow the [official Microsoft guide for Azure Function's extenion](https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=csharp)

## Author

* **Gabriel M De Paoli** - [*github*](github.com/gabrielpaoli-dev)
