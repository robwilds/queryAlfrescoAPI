import peopleGroups
import pandas as pd

from flask import Flask,json,Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/peoplegroups")
def peoplegroups():
    return Response(peopleGroups.main().to_json(orient = 'records'),mimetype='text/json')
    #return json.dumps(peopleGroups.main().to_json(orient = 'records'))