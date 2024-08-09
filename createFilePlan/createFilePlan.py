# this is for the file plan creation from the angular app

from queryAlf import runQuery
import pandas as pd
import json
import os
import io
from dotenv import load_dotenv

baseFilePlanID = "edf97708-412b-461d-9229-fd0b576b73d6"
baseURL = "http://clive-aws-booth.sales-demohyland.com/alfresco/api/-default-/public/gs/versions/1"
def createCategory(filePlanId,classificationgeneral,grsid):
    #for clive site: filePlanId is workspace://SpacesStore/edf97708-412b-461d-9229-fd0b576b73d6

    postURL = baseURL + "/file-plans/"+baseFilePlanID+"/categories"
    #Post = /file-plans/{filePlanId}/categories  
    body="""{{
          "name": "{0}",
          "properties" :
          {{
			"rma:vitalRecordIndicator":"false",
    		"rma:identifier": "{1}"
            }}
 		}}""".format(classificationgeneral,grsid)
    
    print ("***Create Category***->\n"+body);

    print(runQuery('post',postURL,body,'demo','demo'))

def SearchFilePlanId():
    print(NotImplementedError);


def createSubCategoryandRetention(recCategorId):
    #Post: /record-categories/{recordCategoryId}/children
    body="""
{ "name":"$B from spreadsheet", "nodeType":"rma:recordCategory", "hasRetentionSchedule": true
  
} 
"""

    #Post: {{hostname}}/alfresco/s/api/rma/actions/ExecutionQueue
    body="""
    
{
  "name":"createDispositionSchedule",
  "nodeRef":"workspace://SpacesStore/{{recordcategory.id}}" //recordcategory.id is what you saved from the previous call
}
"""

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

#add disposition action for destory
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
    print(NotImplementedError);

def main(inputJson):
    #print(inputJson)
    #df = pd.json_normalize(inputJson)
    #df = pd.read_json( io.StringIO( json.dumps(inputJson) ),orient="records")
    #print(df['GRSID'])

    jsonObject = json.loads(json.dumps(inputJson))

    for key in inputJson:
        #print(key['ClassificationGeneral'],key['GRSID'])
        # now need to run through the processes to create the file plan
        createCategory(baseFilePlanID,key['ClassificationGeneral'],key['GRSID'])


    #return a json list of the nodeids created (for the categories)
    return('{"response":"Create File Plans success"}')


if __name__ == "__main__":
    main() #debug if this file is run directly not from flask app