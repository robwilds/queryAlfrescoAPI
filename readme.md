# Introduction

This python script set will query Alfresco with given query statements.  refer to the app.py file for the provided end points.  This can be utilized with an angular app to get user groups and audit information for a node

All Crud operations are supported but filtering of specific CRUD operations needs to be built out in the queryAlf.py script

## PreReqs

Install python 3.10.5 or higher then...

There's a requirements.txt file ready to go with everything you need to get going. 

run from the command line from the root of the project: pip3 install -r requirements.txt


## Environment Setup

This project is inteded to run as a container (see docker-compose.yml).  within said file are environment variables that should be altered to fit your application

You can also reate a .env file in the root of the project.  There's a envTemplate.txt file that can be used as a starter.

## Process Flow

This project is configure like a micro-service.  Run the app by using the command "flask run" from the command line.  this will fire up the app.py and use the default port of 9600.  you will be able to navigate to an endpoint with http://<hostname>:9600

## Configured EndPoints

access the root of the microservice:  http://<hostname>:9600.  you will see a list of end points that are configured within a swagger interface

## Running the microservice

from the command line at the root of the project:  python3 app.py.  

There's also a docker commands file in the root of the project for you to create a container
