import peopleGroups
import pandas as pd
import auditApps
import auditEntryForNode
import getRekognitionFiles as grf
import createFilePlan
import os
from dotenv import load_dotenv
from flask import Flask,json,Response,request
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint

# Load environment variables from the .env file
load_dotenv()

port=os.getenv("port")
BASE_URL=os.getenv("BASE_URL")

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)

CORS(app)

#add swagger: https://pypi.org/project/flask-swagger-ui/
#swagger tutorial: https://www.youtube.com/watch?v=7MS1Z_1c5CU&list=PLnBvgoOXZNCOiV54qjDOPA9R7DIDazxBA


@app.route("/")
def default():
    return """<h1>{BASE_URL}</h1><p/><h1>Methods available:</h1>
                <p><a href="/peoplegroups">peoplegroups</a></p>
                <p><a href="/auditapps">auditapps</a></p>
                <p><a href="/auditentryfornode">auditentryfornode?nodeid=</a></p><form method="get" action="/auditentryfornode">
    <input type="text" name="nodeid" placeholder="nodeID...." />
    <input type="submit" value="submit" />
</form>
                <p><a href="/createfileplan">createFilePlan</a> this accepts post data</p>
                <p><a href="/getrekognitionfiles">getrekognitionfiles</a></p>""".format(path=request.root_url,BASE_URL=BASE_URL)

@app.route("/peoplegroups")
def peoplegroups():
    return Response(peopleGroups.main().to_json(orient = 'records'),mimetype='text/json')

@app.route("/auditapps")
def auditapps():
    return Response(auditApps.main().to_json(orient = 'records'),mimetype='text/json')

@app.route("/auditentryfornode")
def auditentryfornode():
    nodeID = request.args.get('nodeid')
    return Response(auditEntryForNode.main(nodeID).to_json(orient = 'records'),mimetype='text/json')

@app.route("/createfileplan",methods = ['POST'])
def createFilePlan():
    # test curl command: curl -X POST http://localhost:9600/createfileplan --data-binary "@testDataFromAngular.txt"
    print (request.get_json())
    return Response(request.get_json())

@app.route("/getrekognitionfiles")
def getRekognitionFiles():
    return Response(grf.main(request.root_url).to_json(orient="records"))

if __name__ == "__main__":

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    }
)

    app.register_blueprint(swaggerui_blueprint)

    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=port, debug=True)