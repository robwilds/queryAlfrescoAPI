import peopleGroups
import pandas as pd
import auditApps
import auditEntryForNode
import getRekognitionFiles as grf
import os
from dotenv import load_dotenv
from flask import Flask,json,Response,request
from flask_cors import CORS, cross_origin

# Load environment variables from the .env file
load_dotenv()

port=os.getenv("port")
BASE_URL=os.getenv("BASE_URL")

#add images (static) folder
# https://stackoverflow.com/questions/72794072/python-flask-how-to-dynamically-handle-image-and-folder-generation

app = Flask(__name__)
CORS(app)

#add swagger: https://stackoverflow.com/questions/46237255/how-to-embed-swagger-ui-into-a-webpage


@app.route("/")
def default():
    return """<h1>{BASE_URL}</h1><p/><h1>Methods available:</h1>
                <p><a href="{path}/peoplegroups">peoplegroups</a></p>
                <p><a href="{path}/auditapps">auditapps</a></p>
                <p><a href="{path}/auditentryfornode">auditentryfornode?nodeid=</a></p>
                <p><a href="{path}/createfileplan">createFilePlan</a></p>
                <p><a href="{path}/getrekognitionfiles>getrekognitionfiles</a></p>""".format(path=request.root_url,BASE_URL=BASE_URL)

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

@app.route("/createfileplan")
def createFilePlan():
    print(NotImplementedError)
    return NotImplementedError

@app.route("/getrekognitionfiles")
def getRekognitionFiles():
    return Response(grf.main(request.root_url).to_json(orient="records"))

if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=port, debug=True)