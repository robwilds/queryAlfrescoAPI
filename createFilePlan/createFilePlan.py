# this is for the file plan creation from the angular app

from queryAlf import runQuery
import pandas as pd
import json
import os
import io
from dotenv import load_dotenv

####Variables
baseFilePlanID = "07cbdcf4-e18e-4783-8bdc-f4e18e3783f1"
baseURL = "http://localhost:8080/alfresco/api/-default-/public/gs/versions/1"
recordCategoryID = ""
subRecordID = ""
filePlanID = ""
retentionScheduleID=""
user='admin'
passwd ='admin'

def createCategory(filePlanId,classificationgeneral,grsid) -> str | None:
    #for clive site: filePlanId is workspace://SpacesStore/edf97708-412b-461d-9229-fd0b576b73d6
    #for local in docker on small macbook pro is workspace://SpacesStore/07cbdcf4-e18e-4783-8bdc-f4e18e3783f1

    postURL = baseURL + "/file-plans/"+baseFilePlanID+"/categories?autoRename=true"
    #Post = /file-plans/{filePlanId}/categories  
    body="""{{
          "name": "{0}",
          "properties" :
          {{
			"rma:vitalRecordIndicator":"false",
    		"rma:identifier": "{1}"
            }}
 		}}""".format(classificationgeneral,grsid)
    
    print ("postURL for create category->"+postURL +"   body->\n"+body);

    response = runQuery('post',postURL,body,user,passwd)
    print('response is->'+str(response))

    #print(recordCategoryID)
    return (response['entry']['id'])

def SearchFilePlanId():
    print(NotImplementedError);

def createFilePlan(recCategoryId,retentionYears):
    return('nothing')

def createFolder(recCategoryId):
    return('nothing')

def createSubCategoryandRetention(recCategoryId,recordTitle,fullDispositionInstruction,dispositionAuthority,retentionYears):


    postURL = baseURL+"/record-categories/"+recCategoryId+"/children"
    body="""{{
    "name":"{0}",
    "nodeType":"rma:recordCategory",
    "hasRetentionSchedule": true}}""".format(recordTitle)

    response = runQuery('post',postURL,body,'demo','demo')
    subCategoryId = response['entry']['id']
    print('sub category id->'+ subCategoryId)



    #Now create the disposition schedule

    postURL = baseURL + "/alfresco/s/api/rma/actions/ExecutionQueue"
    body="""{{
  "name":"createDispositionSchedule",
  "nodeRef":"workspace://SpacesStore/{0}"
}}""".format(subCategoryId)
    
    print("body for disposition creation is->"+body)
    print('disposition response is->'+str(runQuery('post',postURL,body,'demo','demo')))





    #get dispositionschedule node id
    body = """Get: {{hostname}}/alfresco/api/-default-/public/alfresco/versions/1/nodes/{{recordcategoryid}}/children?where=(nodeType=rma:dispositionSchedule)"""

    #add retention authority
    #Post: {{hostname}}/alfresco/s/api/node/workspace/SpacesStore/dispositionScheduleNodeId/formprocessor
    body = """
{
  "prop_rma_dispositionAuthority”:"$L"",
  "prop_rma_dispositionInstructions":"$K",
  "prop_rma_recordDisposition":"true"
}

"""

    #add disposition action for cutoff
    #POST /alfresco/s/api/node/{store_type}/{store_id}/{recordcategoryid}/dispositionschedule/dispositionactiondefinitions
    body = """
{
   "name" : “Cutoff”,
   "description" : “$K”,
   "period" : “”
   "periodProperty" : “Immediately”,
   "eligibleOnFirstCompleteEvent" : (Logic in RPA – if $G cell is Event then “and”, “or” otherwise)
   "events" : [List of event names]
}

"""

#add disposition action for destroy
#POST /alfresco/s/api/node/{store_type}/{store_id}/{id}/dispositionschedule/dispositionactiondefinitions

    body = """
{
   "name" : “Destroy”,
   "description" : “$K”,
   "period" : “$F from sheet”
   "periodProperty" : “{http://www.alfresco.org/model/recordsmanagement/1.0}cutOffDate”:,
   "eligibleOnFirstCompleteEvent" : (Logic in RPA – if $G cell is Event then “and”, “or” otherwise)
   "events" : “$H from sheet”
}

"""
    #print(NotImplementedError);

def main(inputJson):
    #print(inputJson)
    #df = pd.json_normalize(inputJson)
    #df = pd.read_json( io.StringIO( json.dumps(inputJson) ),orient="records")
    #print(df['GRSID'])

    jsonObject = json.loads(json.dumps(inputJson))

    for key in inputJson:
        #print(key['ClassificationGeneral'],key['GRSID'])

        # now need to run through the processes to create the file plan
        recordCategoryID = createCategory(baseFilePlanID,key['ClassificationGeneral'],key['GRSID'])
        print ('record cat id is->'+recordCategoryID)

        # now create the subcategory using the same createCategory function
        subRecordID = createCategory(recordCategoryID,'','')
        print ('sub rec category id is->' + subRecordID)

        #Process the sub category with the file plan - this is one huge routine which could be broken up
        #createSubCategoryandRetention(recordCategoryID,key['RecordTitle'],key['FullDispositionInstruction'],key['DispositionAuthority'],key['RetentionYears'])



    #return a json list of the nodeids created (for the categories)
    return('{"response":"Create File Plans success"}')


if __name__ == "__main__":
    main() #debug if this file is run directly not from flask app