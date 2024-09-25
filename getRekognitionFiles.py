from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv
import requests,json
from requests.auth import HTTPBasicAuth
import elastic.sendDatatoElastic as send2Elastic

#test nodeid in rwilds232: 19264eec-0d3e-4afe-80df-acc72c4e950b

# Load environment variables from the .env file
load_dotenv()

BASE_URL= os.getenv("BASE_URL")
auth = os.getenv("auth")
user = os.getenv("user")
passwd = os.getenv("pass")
devpath = os.getenv("devpath")
prodpath = os.getenv("prodpath")
path = prodpath # set the working path here once!

rekogSrc= []
rekogName= []
rekogLabels = []
rekogParent = []
rekogNodeId = []
rekogModifiedDate = []
cols = {0: 'src',1:'name',2:'labels',3:'parentId',4:'nodeId',5:'modifiedDate'}

def downloadImages(nodeid,path):

  url = BASE_URL + "/alfresco/api/-default-/public/alfresco/versions/1/nodes/"+nodeid+"/content"
  temp4 = requests.get(url,auth = (user, passwd))

  #print(temp4.text)

  #put process here to determine extension based on mimetype
  #could use this: https://note.nkmk.me/en/python-mimetypes-usage/

  #check if file is already there, otherwise skip it
  #this could be bad if an existing node gets a new file
  filePath = path + nodeid+".jpg"
  fileName = nodeid+".jpg"
  if os.path.exists(filePath):
    print('file already exists-> '+filePath+'\n')
  else:
    print('file doesn''t exist-> '+filePath+'\n')
    with open(filePath,'wb') as f:
      f.write(temp4.content)

  return fileName

def cleanFolder(path):
  for i in os.listdir(path):
    if ".json" not in i:
      print("removing file: "+i)
      os.remove(path+i)

def pullListofrekogfiles():
  imageQuery = BASE_URL + '/alfresco/api/-default-/public/search/versions/1/search'
  postData = """{
  "query": {
    "query": "ASPECT:'ai:labels'"
  }
  }"""

  data=runQuery('post',imageQuery,postData,user,passwd)
  #print ('query url is: ' + imageQuery + '--->>>>' + postData) #debug
  return data

def getrekogfilesinfo(nodeid):
  nodeInfoQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/nodes/' + nodeid +'?fields=properties,name,id,modifiedAt' #use fileIds to limit the amount of data returned

  data=runQuery('get',nodeInfoQuery,'',user,passwd)

  print ('\n\ndata from alfresco -->' + json.dumps(data)) #debugging
  return data;

def createPath(path):
  if not os.path.exists(path):
    os.makedirs(path)
    print(path + ' Created')

def getTagValue(tagidArray):

  #loop through each entry to get the name and add to array then return array
  tagvalArray = []

  for entry in tagidArray:
    tagvaluequery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/tags/'+entry
    data = runQuery('get',tagvaluequery,'',user,passwd)
    tagvalArray.append(data['entry']['tag'])
  
  #print ('\n data from Tag routine -> '+str(tagvalArray))
  return tagvalArray


def main(requestURL="Http://localllll/"): #the hardcode url is in place for running from command line not from flask

  #clear arrays now!
  rekogSrc = []
  rekogLabels = []
  rekogName = []
  rekogParent = []
  rekogNodeId = []
  rekogModifiedDate = []

  runOnce = False

  docPayload = ""

  #create the storage path for the downloaded files
  createPath(path)
  
  #clean the download folder now!
  #cleanFolder(path)

  #print('search result --> ' + json.dumps(pullListofrekogfiles())) #debug
  #now loop and get all images to download and populate data frame columns
  counter = 1
  for entry in pullListofrekogfiles()['list']['entries']:
    #print('node-> ' + entry['entry']['id'] + ' labels-> ' + str(getrekogfilesinfo(entry['entry']['id'])['entry']['properties']['schema:label'])) #debugging
    rekogSrc.append(requestURL+'static/' + downloadImages(entry['entry']['id'],path))
    rekogName.append(entry['entry']['name'])

    
    #rekogLabels.append(getrekogfilesinfo(entry['entry']['id'])['entry']['properties']['schema:label'])
    
    rekogLabels.append(getTagValue(getrekogfilesinfo(entry['entry']['id'])['entry']['properties']['cm:taggable']))
    
    #print('Tag value from caller -> ' + getTagValue(getrekogfilesinfo(entry['entry']['id'])['entry']['properties']['cm:taggable']))
    #added to identify hyland employees
    #print ('\\n\\n debug for schema:textLines -> '+ str(getrekogfilesinfo(entry['entry']['id'])['entry']['properties']['cm:taggable']))
    #rekogLabels.append(getrekogfilesinfo(entry['entry']['id'])['entry']['properties']['schema:textLines'])
    rekogParent.append(entry['entry']['parentId'])
    rekogNodeId.append(entry['entry']['id'])
    rekogModifiedDate.append(entry['entry']['modifiedAt'])

    # So we have all the information now, but we need to build the elastic payload for each record
    #for index in range(len(rekogLabels)):
    
    #print('label list ->' + str(rekogLabels).split(','))

    #print('split info for labels -> \n')

    for i in str(rekogLabels).split(','):
      currentTag = i.replace('[','').replace(']','').replace('\'','').strip()

      #print(currentTag)

      doc = {
    'name': '\''+rekogName[-1]+'\'',
    'tag': '\''+currentTag+'\'',
}
      send2Elastic.sendIndRecToelastic(doc,counter)
      counter = counter + 1
      #doc = "" #flush doc now


  #print ('doc payload is -> '+ docPayload)

  #send2Elastic.main(docPayload)

 
  # now feed docpayload to elastic

  rekogDF = pd.DataFrame([rekogSrc,rekogName,rekogLabels,rekogParent,rekogNodeId,rekogModifiedDate]).T
  rekogDF.rename(columns=cols,inplace=True)

  #print (rekogDF)
  #rekogDF.to_excel('rekogfiles.xlsx')

  return rekogDF

if __name__ == "__main__":
  main()
