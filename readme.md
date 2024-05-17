# Introduction

This python script set will query Alfresco with given query statements.  refer to the app.py file for the provided end points.  This can be utilized with an angular app to get user groups and audit information for a node

All Crud operations are supported but filtering of specific CRUD operations needs to be built out in the queryAlf.py script


## PreReqs

python 3.10.5 or greater
pip 22.04 or greater
json
pandas
python-dotenv
openpyxl
flask
flask-cors

## Environment Setup
be sure to create a .env file in the root of the project with 
BASE_URL= (for example: "http://yourAlfrescoURL.com")
auth= (this is the base64 encode of the user password for example: "xeofhSRgsd")

## Process Flow

This project is configure like a micro-service.  Run the app by using flask run from the command line.  this will fire up the app.py and use the default port of 5000.  

there's are two end points configured:

peopleGroups:  this returns a list of all user with associated groups.  filtering will be added later
auditentryfornode/nodeid={nodeid}: this will fetch all audit actions, action dates and reiterate the username for the given nodeid.  nodeid must be provided


