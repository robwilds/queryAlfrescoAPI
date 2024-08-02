# this is for the file plan creation from the angular app

from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv

def createCategory(filePlanId):
    #Post = /file-plans/{filePlanId}/categories  
    body=""" 
{
          “name”: “$C (classification) cell in spreadsheet”,
         “description”: “This is a automated creation of record category $C cell in spreadsheet + $A cell in spreadsheet (substring where we would leave out the last 3 digits)
          “ properties” : 
	 	{
			"rma:vitalRecordIndicator":"false",
    			“rma:identifier”: “”$A cell in spreadsheet (substring where we would leave out the last 3 digits)”
}
 		}

"""
    print (NotImplementedError);

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



def main():
    print("nothing");




if __name__ == "__main__":
    main() #debug if this file is run directly not from flask app