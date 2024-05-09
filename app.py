import peopleGroups
import pandas as pd

from flask import Flask,json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/peoplegroups")
def peoplegroups():
    return json.dumps(peopleGroups.main().to_json(orient = 'records'))