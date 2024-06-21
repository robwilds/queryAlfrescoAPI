import peopleGroups
import pandas as pd
import auditApps
import auditEntryForNode
import getRekognitionFiles

from flask import Flask,json,Response,request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

#add swagger: https://stackoverflow.com/questions/46237255/how-to-embed-swagger-ui-into-a-webpage


@app.route("/")
def default():
    return """<h1>Methods available:</h1>
                <p>peoplegroups</p>
                <p>auditapps</p>
                <p>auditentryfornode</p>
                <p>createFilePlan</p>
                <p>getrekognitionfiles</p>"""

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

@app.route("/createFilePlan")
def createFilePlan():
    print(NotImplementedError)
    return NotImplementedError

@app.route("/getrekognitionfiles")
def getRekognitionFiles():
    return getRekognitionFiles()

if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=5202, debug=True)