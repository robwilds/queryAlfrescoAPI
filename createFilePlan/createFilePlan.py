# this is for the file plan creation from the angular app

from queryAlf import runQuery
import pandas as pd
import json
import os
import io
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

BASE_URL= os.getenv("BASE_URL")
user=os.getenv("user")
passwd=os.getenv("pass")

####Variables
baseFilePlanID = os.getenv("baseFilePlanID")
#BASE_URL = "http://localhost:8080/alfresco/api/-default-/public/gs/versions/1"
recordCategoryID = ""
subRecordID = ""
subFolderID = ""
filePlanID = ""
retentionScheduleID=""

def createCategory(filePlanId,classificationgeneral,grsid) -> str | None:
    #for clive site: filePlanId is workspace://SpacesStore/edf97708-412b-461d-9229-fd0b576b73d6
    #for local in docker on small macbook pro is workspace://SpacesStore/07cbdcf4-e18e-4783-8bdc-f4e18e3783f1

    postURL = BASE_URL + "/alfresco/api/-default-/public/gs/versions/1/file-plans/"+baseFilePlanID+"/categories?autoRename=true"
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
    print('response is->'+str(response)+'\n')

    #print(recordCategoryID)
    return (response['entry']['id'])

def SearchFilePlanId():
    print(NotImplementedError);

def createFilePlan(recCategoryId,retentionYears):
    return('nothing')

def createFolder(recSubCategoryId,name):
    postURL = BASE_URL+"/alfresco/api/-default-/public/gs/versions/1/record-categories/"+recSubCategoryId+"/children"
    body="""{{
    "name":"{0}",
    "nodeType":"rma:recordFolder"}}""".format(name)

    response = runQuery('post',postURL,body,user,passwd)
    print('response from folder call is->'+str(response)+'\n')
    subFolderID = response['entry']['id']
    
    return(subFolderID)

def createSubCategory(recCategoryId,recordTitle):
    postURL = BASE_URL+"/alfresco/api/-default-/public/gs/versions/1/record-categories/"+recCategoryId+"/children"
    body="""{{
    "name":"{0}",
    "nodeType":"rma:recordCategory",
    "hasRetentionSchedule": true}}""".format(recordTitle)

    response = runQuery('post',postURL,body,user,passwd)
    print('response from sub category call is->'+str(response)+'\n')
    subCategoryId = response['entry']['id']
    #print('sub category id->'+ subCategoryId)
    return(subCategoryId)

def createRetentionSchedule(subRecCategoryId,dispositionAuthority,fullDispositionInstruction,isrecordlevel):
    postURL = BASE_URL+"/alfresco/api/-default-/public/gs/versions/1/record-categories/"+subRecCategoryId+"/retention-schedules"
    #cleans the retention instructions now
    fullDispositionInstruction = fullDispositionInstruction.replace('"','')
    if (isrecordlevel):
        isrecordlevel = "true"
    else:
        isrecordlevel = "false"

    body="""{{
      "authority": "{0}",
      "instructions": "{1}",
      "isRecordLevel": {2}
  }}""".format(dispositionAuthority,fullDispositionInstruction,isrecordlevel)
    
    response = runQuery('post',postURL,body,user,passwd)
    print('response from retention schedule call is->'+str(response)+'\n'+'with body->'+body+'\n')
    retentionScheduleID = response['entry']['id']
    #print('sub category id->'+ subCategoryId)
    return(retentionScheduleID)
    
def createRetentionStep(retentionScheduleID,retentionType,retentionTime,retentionPeriod,description):
    postURL = BASE_URL+"/alfresco/api/-default-/public/gs/versions/1/retention-schedules/"+retentionScheduleID+"/retention-steps"

    body="""{{
      "name":"{retentionType}",
      "description":"{description}",
      "periodAmount": {retentionTime},
      "period":"{retentionPeriod}",
      "periodProperty":"cm:created",
      "combineRetentionStepConditions": false,
      "events":[],
      "eligibleOnFirstCompleteEvent": true    
  }}""".format(retentionType=retentionType,retentionTime=retentionTime,description=description,retentionPeriod=retentionPeriod)
    
    response = runQuery('post',postURL,body,user,passwd)
    print('response from retention retention step call is->'+str(response)+'\n'+'with body->'+body+'\n')
    retentionStepID = response['entry']['id']
    #print('sub category id->'+ subCategoryId)
    return(retentionStepID)

def main(inputJson):
    #print(inputJson)
    #df = pd.json_normalize(inputJson)
    #df = pd.read_json( io.StringIO( json.dumps(inputJson) ),orient="records")
    #print(df['GRSID'])

    jsonObject = json.loads(json.dumps(inputJson))

    print('captured json is->'+str(jsonObject)+'\n')

    for key in inputJson:
        #print(key['ClassificationGeneral'],key['GRSID'])

        # now need to run through the processes to create the file plan
        recordCategoryID = createCategory(baseFilePlanID,key['RecordTitle'],key['GRSID'])
        print ('record cat id is->'+recordCategoryID)

        # now create the subcategory using the same createCategory function
        subRecordID = createSubCategory(recordCategoryID,key['ClassificationGeneral'])
        print ('sub rec category id is->' + subRecordID)

        # now add the retention schedule
        retentionScheduleID = createRetentionSchedule(subRecordID,key['DispositionAuthority'],key['FullDispositionInstruction'],True)
        print('retention schedule id is->'+retentionScheduleID)
        
        # now add the CUTOFF step
        retentionStepsID = createRetentionStep(retentionScheduleID,"cutoff",0,'immediately','cutoff immediately')
        print('retention step id for cutoff is->'+retentionStepsID)

        # now add the Destroy step
        retentionStepsID = createRetentionStep(retentionScheduleID,"transfer",key['RetentionYears'],"year",'transfer in 3 years or whatever')
        print('retention step id for destroy is->'+retentionStepsID)

        # now put the folder on the subcategory..call it "all records" for now
        subFolderID = createFolder(subRecordID,'AllRecords')
        print ('sub folder id is->'+subFolderID)


    #return a json list of the nodeids created (for the categories)
    return('{"response":"Create File Plans success"}')


if __name__ == "__main__":
    main() #debug if this file is run directly not from flask app