# this is the main file...all other procedures are called from here
from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

BASE_URL= os.getenv("BASE_URL")
auth = os.getenv("auth")


def pullGroups():
    groupQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/groups'
    name,id = [],[]

    print ('query url is: ' + groupQuery + '--->>>>')
    data=runQuery('get',groupQuery,'',auth)
    #jdata = json.loads(data)
    #print ('data -->>> ')

    #now loop through the results and apply to panda dataframe
    #for entry in data['list']['entries']:
        
        #name.append(entry['displayName'])
        #id.append(entry['id'])
        #tempdata = json.dumps(entry)

        #print (entry)

    #groupFrame = pd.DataFrame([name],[id])

    return data

def pullPeople():
    peopleQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/people?skipCount=0&maxItems=100000'
    print ("pull people URL is: " + peopleQuery)
    data = runQuery('get',peopleQuery,'',auth)
    return data
    
def pullPeopleGroups(personid):
    peopleGroupsQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/people/'+personid+'/groups'
    print ("pull peopleGroups URL is: " + peopleGroupsQuery)
    data = runQuery('get',peopleGroupsQuery,'',auth)
    return data

def main():

    #print (pullGroups())
    #print (pullPeople())

    #need to input people into a dataframe

    #now pass every people ID and pass to dataframe
    for item in pullPeopleGroups('demo')['list']['entries']:
        #print (item) #debugging

        #print (item['entry']['id'] + ' - ' + str(item['entry']['isRoot']) + ' - ' + item['entry']['displayName'])
        print(item['entry']['id'])

    #now need to merge and output
    
if __name__ == "__main__":
    main()