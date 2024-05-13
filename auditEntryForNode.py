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
appEntryDate = []
appEntryUser = []

cols = {0: 'nodeID',1:'auditEntryID',2:'entryDate',3:'details',4:'user'}

def pullAuditEntryForNode(nodeid):

    auditEntryforNodeQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/nodes/'+nodeid+'/audit-entries'

    #print ('query url is: ' + auditentryfornodeQuery + '--->>>>') #debug
    data=runQuery('get',auditEntryforNodeQuery,'',auth)
    #print (data) #debug
    return data

def pullAuditEntryDetailsForNode(auditentryid):

    auditEntryDetailsForNodeQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/audit-applications/alfresco-access/audit-entries/'+str(auditentryid)+'?fields=values'

    data=runQuery('get',auditEntryDetailsForNodeQuery,'',auth)

    #See if the actual action data can be returned
    actionDetailsForNode = data['entry']['values']['/alfresco-access/transaction/action']
    actionUserForNode = data['entry']['values']['/alfresco-access/transaction/user']

    return [actionDetailsForNode,actionUserForNode]

def main(nodeid):
    
    for entry in pullAuditEntryForNode(nodeid)['list']['entries']:
        #print(nodeid + '-' + str(entry['entry']['id'])) #debug

        #set the entry details and user now so there's one call
        entryDetails = pullAuditEntryDetailsForNode(entry['entry']['id'])[0]
        entryUser = pullAuditEntryDetailsForNode(entry['entry']['id'])[1]

        nodeID.append(nodeid) #this will be the same nodeid for each audit entry id
        appEntryID.append(entry['entry']['id'])
        appEntryDate.append(entry['entry']['createdAt'])
        appEntryDetails.append(entryDetails)
        appEntryUser.append(entryUser)
    
    auditentryfornodeDF = pd.DataFrame([nodeID,appEntryID,appEntryDate,appEntryDetails,appEntryUser]).T
    auditentryfornodeDF.rename(columns=cols,inplace=True)

    print (auditentryfornodeDF)
    auditentryfornodeDF.to_excel('auditentryfornode.xlsx')
    return auditentryfornodeDF

if __name__ == "__main__":

    #nodeid = '7a0eb8ca-8b69-43b4-8062-4b79cbddc750' #testing node on rwilds232
    main('7a0eb8ca-8b69-43b4-8062-4b79cbddc750') #debug if this file is run directly not from flask app