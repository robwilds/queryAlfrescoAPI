from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv
import requests,json
from requests.auth import HTTPBasicAuth

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
cols = {0: 'src',1:'name',2:'labels'}

def downloadImages(nodeid,path):

  url = BASE_URL + "/alfresco/api/-default-/public/alfresco/versions/1/nodes/"+nodeid+"/content"
  temp4 = requests.get(url,auth = (user, passwd))

  #print(temp4.text)

  #put process here to determine extension based on mimetype
  #could use this: https://note.nkmk.me/en/python-mimetypes-usage/

  with open(path+'rekogimages/' + nodeid+".jpg",'wb') as f:
    f.write(temp4.content)

  return nodeid+".jpg"

def cleanFolder(path):
  for i in os.listdir(path+'rekogimages/'):
    print("removing file: "+i)
    os.remove(path+'rekogimages/'+i)

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
  nodeInfoQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/nodes/' + nodeid +'?fields=properties'

  data=runQuery('get',nodeInfoQuery,'',user,passwd)

  #print ('data from file info -->' + json.dumps(data)) #debugging
  return data;

def main():

  rekogSrc = [] #clear array now!
  rekogLabels = []
  rekogName = []
  #clean the download folder now!
  #cleanFolder(path)

  #print('search result --> ' + json.dumps(pullListofrekogfiles())) #debug
  #now loop and get all images to download and populate data frame columns
  for entry in pullListofrekogfiles()['list']['entries']:
    #print('node-> ' + entry['entry']['id'] + ' labels-> ' + str(getrekogfilesinfo(entry['entry']['id'])['entry']['properties']['schema:label'])) #debugging
    rekogSrc.append(downloadImages(entry['entry']['id'],path))
    rekogName.append(entry['entry']['name'])
    rekogLabels.append(getrekogfilesinfo(entry['entry']['id'])['entry']['properties']['schema:label'])

  rekogDF = pd.DataFrame([rekogSrc,rekogName,rekogLabels]).T
  rekogDF.rename(columns=cols,inplace=True)

  print (rekogDF)
  #rekogDF.to_excel('rekogfiles.xlsx')

  return rekogDF

if __name__ == "__main__":
  main()
