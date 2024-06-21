from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

BASE_URL= os.getenv("BASE_URL")
auth = os.getenv("auth")
user=os.getenv("user")
passwd=os.getenv("pass")

appID = []
cols = {0: 'appid'}

def pullAuditApps():
    auditAppQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/audit-applications'

    #print ('query url is: ' + auditAppQuery + '--->>>>') #debug
    data=runQuery('get',auditAppQuery,'',user,passwd)
    return data

def main():
    
    appID = [] #clear app id now!
    
    for entry in pullAuditApps()['list']['entries']:
        print(entry['entry']['id'])
        appID.append(entry['entry']['id'])
    
    auditIDDF = pd.DataFrame([appID]).T
    auditIDDF.rename(columns=cols,inplace=True)

    print (auditIDDF)
    auditIDDF.to_excel('auditApps.xlsx')
    return auditIDDF

if __name__ == "__main__":
    main()