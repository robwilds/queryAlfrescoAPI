from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

BASE_URL= os.getenv("BASE_URL")
auth = os.getenv("auth")

nodeID = []
appEntryID = []
appEntryDetails = []

cols = {0: 'auditEntryID',1:'nodeID',2:'details'}

def pullAuditEntryForNode(nodeid):

    auditEntryforNodeQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/nodes/'+nodeid+'/audit-entries'

    #print ('query url is: ' + auditentryfornodeQuery + '--->>>>') #debug
    data=runQuery('get',auditEntryforNodeQuery,'',auth)
    #print (data) #debug
    return data

def pullAuditEntryDetailsForNode(auditentryid):

    auditEntryDetailsForNodeQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/audit-applications/alfresco-access/audit-entries/'+str(auditentryid)+'?fields=values'

    data=runQuery('get',auditEntryDetailsForNodeQuery,'',auth)

    return data

def main(nodeid):
    
    for entry in pullAuditEntryForNode(nodeid)['list']['entries']:
        #print(nodeid + '-' + str(entry['entry']['id'])) #debug

        nodeID.append(nodeid) #this will be the same nodeid for each audit entry id
        appEntryID.append(entry['entry']['id'])
        appEntryDetails.append(pullAuditEntryDetailsForNode(entry['entry']['id']))
    
    auditentryfornodeDF = pd.DataFrame([appEntryID,nodeID,appEntryDetails]).T
    auditentryfornodeDF.rename(columns=cols,inplace=True)

    print (auditentryfornodeDF)
    return auditentryfornodeDF

if __name__ == "__main__":

    #nodeid = '7a0eb8ca-8b69-43b4-8062-4b79cbddc750' #testing node on rwilds232
    main('7a0eb8ca-8b69-43b4-8062-4b79cbddc750')