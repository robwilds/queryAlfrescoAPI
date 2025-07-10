from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv
import requests,json


def getComments(nodeid):
    url = os.getenv("BASE_URL") + "/alfresco/api/-default-/public/alfresco/versions/1/nodes/"+nodeid+"/comments"
    temp4 = requests.get(url,auth = (os.getenv("user"), os.getenv("pass")))
    return temp4
