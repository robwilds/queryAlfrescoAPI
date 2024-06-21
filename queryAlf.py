#this is used like a service to query alfresco rest api
import requests,json
from requests.auth import HTTPBasicAuth

def runQuery(type,queryURL,body,user,passwd):
  basic = HTTPBasicAuth(user, passwd)
  data = ""

  #now run the query to get the raw json data
  match type:
    case 'get':
      data = requests.get(queryURL,auth=basic).json()
      #print(json.dumps(data))
      return data
    case 'post':
      data=requests.post(queryURL,body,auth=basic).json()
      return data
