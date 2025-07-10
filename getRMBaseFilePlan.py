import os
from  queryAlf import runQuery
from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

def getRMBase():
    RMBaseQueryPath = os.getenv("BASE_URL") + '/alfresco/api/-default-/public/search/versions/1/search'
    RMBaseQuery = os.getenv("baseFilePlanQuery")

    print ('Find base RM path id->' + RMBaseQueryPath + ' and query string is: ' +RMBaseQuery + '\n') #debug
    data=runQuery('post',RMBaseQueryPath,RMBaseQuery,os.getenv("user"),os.getenv("pass"))

    if 'error' in str(data):
        print('error found returning the baseFilePlanID from environment variable->'+str(data))
        return os.getenv("baseFilePlanID")
    else:

        for entry in data['list']['entries']:
            print(entry['entry']['id'])
            return entry['entry']['id']

if __name__ == "__main__":
    getRMBase()