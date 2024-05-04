#this is used like a service to query alfresco rest api
import requests,json
from requests.auth import HTTPBasicAuth

def runQuery(type,queryURL,body,auth):
  basic = HTTPBasicAuth('demo', 'demo')
  data = ""

  #now run the query to get the raw json data
  match type:
    case 'get':
      data = requests.get(queryURL,auth=basic).json()
      #print(json.dumps(data))
      return data