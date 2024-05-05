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
    peopleID = []
    peopleStatus = []
    groupID = []
    groupDisplayName = []
    peopleGroupID = []
    peopleGroupName = []

    file_name = 'peopleGroups.xlsx'

    #print (pullGroups()) #may not need this pull if merging people to groups
    #print (pullPeople())

    for entry in pullPeople()['list']['entries']:
        #print (entry['entry']['id'] + ' ' + str(entry['entry']['enabled']))

        #now load each user into a dataframe for People
        peopleID.append(entry['entry']['id'])
        peopleStatus.append(entry['entry']['enabled'])

    #need to input people into a dataframe
    #peopleDF = pd.DataFrame([peopleID,peopleStatus]).T

    #print(peopleDF) #Debug: display people DataFrame

    #now loop through each username and pass to pull people groups


    for person in peopleID:

        for item in pullPeopleGroups(person)['list']['entries']:
            #print (item) #debugging
            #print(person + ' - ' + item['entry']['id']) #debug
            peopleGroupID.append(person)
            peopleGroupName.append(item['entry']['id'])

    #now need to merge and output
    peopleGroupDF = pd.DataFrame([peopleGroupID,peopleGroupName]).T

    print (peopleGroupDF)
    peopleGroupDF.to_excel(file_name)
    
if __name__ == "__main__":
    main()