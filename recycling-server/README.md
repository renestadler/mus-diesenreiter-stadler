# Recycling Server

This module provides endpoints for the retrieval of products by their barcode.
The provided data contains the name of the product as well as the recycling information.

<br/>
<br/>

## Prerequisites
We recommend using [IntelliJ IDEA](https://www.jetbrains.com/de-de/idea/) as an IDE. 

Furthermore, ensure that you have Java 17 installed to execute this program.

Also, by default a Postgresql is used to store data. 
We recommend to start the database in docker by using following command.

```shell
docker run --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres
```

<br/>
<br/>

## Getting started
1. Ensure that the database is started
2. Start the program by running the main file

<br/>
<br/>

## Functionality
This service provides following endpoint.
The code is a custom string. If data is found in the 
OpenFoodFacts API, this data is stored in the database 
and returned. If this already happened, the entry from
the database is returned.

```http request
GET http://localhost:8080/product?barcode=<code>
```

For example, this request will fetch you some info on Nutella.
```http request
GET using http://localhost:8080/product?barcode=3017620422003
```

<br/>
<br/>

## Deploy the application
This application can simply be deployed, by running following commands

```shell
./gradlew build

docker build --build-arg JAR_FILE=build/libs/*.jar -t <projectname>/recycling-server .

docker push <projectname>/recycling-server
```

Then, the application can simply be deployed at a cloud provider by using the uploaded docker image.
