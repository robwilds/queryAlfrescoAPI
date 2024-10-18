import peopleGroups
import pandas as pd
import auditApps
import auditEntryForNode
import getRekognitionFiles as grf
import createFilePlan.createFilePlan as CFP
import getCommentsForNode
import os
from dotenv import load_dotenv
from flask import Flask,jsonify,Response,request,redirect
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
import elastic.sendDatatoElastic as elastic

# Load environment variables from the .env file
load_dotenv()

port=os.getenv("port")
BASE_URL=os.getenv("BASE_URL")

SWAGGER_URL = '/api-explorer'  # URL for exposing Swagger UI (without trailing '/')
API_URL = os.getenv("API_URL")  # Our API url (can of course be a local resource)

app = Flask(__name__)

CORS(app)


@app.route("/")

def default():
    return redirect("/api-explorer")

@app.route("/peoplegroups")
def peoplegroups():
    return Response(peopleGroups.main().to_json(orient = 'records'),mimetype='text/json')

@app.route("/auditapps")
def auditapps():
    return Response(auditApps.main().to_json(orient = 'records'),mimetype='text/json')

@app.route("/auditentryfornode")
def auditentryfornode():
    nodeID = request.args.get('nodeid')
    print('node id for audit is->'+nodeID)
    return Response(auditEntryForNode.main(nodeID).to_json(orient = 'records'),mimetype='text/json')

@app.route("/getrekognitionfiles")
def getRekognitionFiles():
    return Response(grf.main(request.root_url).to_json(orient="records"))

@app.route("/clearelastic")
def clearelastic():
    return Response(elastic.clearIndexes() )

@app.route("/getcomments/<nodeid>")
def getcomments(nodeid):
    return Response(getCommentsForNode.getComments(nodeid))

@app.route("/analyzetext",methods = ['POST','OPTIONS'])
@cross_origin()
def analyzetext():
    #https://medium.com/@penkow/how-to-run-llama-2-locally-on-cpu-docker-image-731eae6398d1
    print("\nanalyze text not implemented")
    return Response("not implemented yet")

@app.route("/createfileplan",methods = ['POST','OPTIONS'])
@cross_origin()
def createFilePlan():
    # test curl command: curl -X POST -H 'Content-Type: application/json' http://localhost:9600/createfileplan --data-binary "@testDataFromAngular.txt"
    #print (request.get_json())
    #return Response(request.get_json())
    
    return Response(CFP.main(request.get_json()))

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