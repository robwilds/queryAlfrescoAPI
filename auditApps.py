from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

BASE_URL= os.getenv("BASE_URL")
auth = os.getenv("auth")

appID = []
cols = {0: 'appid'}

def pullAuditApps():
    auditAppQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/audit-applications'

    #print ('query url is: ' + auditAppQuery + '--->>>>') #debug
    data=runQuery('get',auditAppQuery,'',auth)
    return data

def main():
    
    for entry in pullAuditApps()['list']['entries']:
        print(entry['entry']['id'])
        appID.append(entry['entry']['id'])
    
    auditIDDF = pd.DataFrame([appID]).T
    auditIDDF.rename(columns=cols,inplace=True)

    print (auditIDDF)
    return auditIDDF

if __name__ == "__main__":
    main()