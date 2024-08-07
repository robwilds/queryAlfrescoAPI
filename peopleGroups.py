# this is the main file...all other procedures are called from here
from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

BASE_URL= os.getenv("BASE_URL")
user=os.getenv("user")
passwd=os.getenv("pass")

def pullGroups():
    groupQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/groups'
    name,id = [],[]

    #print ('query url is: ' + groupQuery + '--->>>>') #debug
    data=runQuery('get',groupQuery,'',user,passwd)

    return data

def pullPeople():
    peopleQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/people?skipCount=0&maxItems=100000'
    #print ("pull people URL is: " + peopleQuery) #debug
    data = runQuery('get',peopleQuery,'',user,passwd)
    return data
    
def pullPeopleGroups(personid):
    peopleGroupsQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/people/'+personid+'/groups'
    #print ("pull peopleGroups URL is: " + peopleGroupsQuery) #debug
    data = runQuery('get',peopleGroupsQuery,'',user,passwd)
    return data

def main():
    peopleID = []
    peopleStatus = []
    peopleGroupID = []
    peopleGroupName = []
    peopleGroupStatus = []

    file_name = 'peopleGroups.xlsx'
    cols = {0: 'user', 1: 'status',2:'group'}
    for entry in pullPeople()['list']['entries']:

        #now load each user into array for user later
        peopleID.append(entry['entry']['id'])
        peopleStatus.append(entry['entry']['enabled'])

    #now loop through each username and pass to pull people groups
    for person in peopleID:

        for item in pullPeopleGroups(person)['list']['entries']:
            #print (item) #debugging
            #print(person + ' - ' + item['entry']['id']) #debugging
            peopleGroupID.append(person)
            peopleGroupStatus.append(peopleStatus[list(peopleID).index(person)]) #list(poepleid).index(person) will get the person's status for the matching index
            peopleGroupName.append(item['entry']['id'])

    #now create the dataframe with pandas
    peopleGroupDF = pd.DataFrame([peopleGroupID,peopleGroupStatus,peopleGroupName]).T
    peopleGroupDF.rename(columns=cols,inplace=True)

    print (peopleGroupDF)
    peopleGroupDF.to_excel(file_name)
    #peopleGroupDF.to_html(file_name+'.html')

    return peopleGroupDF

if __name__ == "__main__":
    main()