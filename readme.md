# Introduction

This python script set will query Alfresco with given query statements.  

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

edit the main.py file with the query you need and pass to the queryAlf function.  The data returned will be a python dictionary object.

