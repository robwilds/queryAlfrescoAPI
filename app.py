import peopleGroups
import pandas as pd
import auditApps
import auditEntryForNode

from flask import Flask,json,Response,request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/peoplegroups")
def peoplegroups():
    return Response(peopleGroups.main().to_json(orient = 'records'),mimetype='text/json')

@app.route("/auditapps")
def auditapps():
    return Response(auditApps.main().to_json(orient = 'records'),mimetype='text/json')

@app.route("/auditentryfornode", methods=('get', 'post'))
def auditentryfornode():
    nodeID = request.args.get('nodeid')
    return Response(auditEntryForNode.main(nodeID).to_json(orient = 'records'),mimetype='text/json')