# Import necessary libraries
import pandas as pd  # For data manipulation with DataFrames
from elasticsearch import Elasticsearch, helpers
import configparser
import json
import time

config = configparser.ConfigParser()
print ('config parsed-> ' + str(config))
config.read('elastic.ini')

es = Elasticsearch(
  #cloud_id=config['ELASTIC']['cloud_id'],
  #http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password']))
  cloud_id = '''9ce78c3f7ab445339ebb510a901604fd:dXMtZWFzdC0yLmF3cy5lbGFzdGljLWNsb3VkLmNvbSQ3N2QxZDJiNGZjNWI0M2IxYmJiZjFmZDc1MzE1NmMyNyRhOTIyOWE3OWU1NTM0YjBlYTRmZTZlZjBlNjU1OTUxNQ==''',
  http_auth = ('enterprise_search','hylandforce1')
  )
       
def gendata(docs,optype="index",ind="samplerekog"):
    #docs = [{"name": "Rob", "tag": "male"},{"name": "Rob", "tag": "weapon"}]
    for doc in docs:
        yield {
            "_op_type":optype,
            "_index": index,
            "doc": doc
        }

def clearIndexes(ind="samplerekog"):
    #clear the index(ces)
    indices = [ind]
    return(es.delete_by_query(index=indices, body={"query": {"match_all": {}}}))

def sendIndRecToelastic(doc,id):
    """ doc = {
    'name': 'Rob',
    'tag': 'male'
} """
    resp = es.index(index="samplerekog", id=id, document=doc)
    print(resp['result'])

def main(docs,index="samplerekog"):

  #print("bulk doc is -> " + str(bulkdocument))
  # Create an Elasticsearch client using the provided credentials
  #es = Elasticsearch(cloud_id=elasticID, api_key=elasticKey) #use this for api key access
  """ es = Elasticsearch(
  #cloud_id=config['ELASTIC']['cloud_id'],
  #http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password']))
  cloud_id = '''9ce78c3f7ab445339ebb510a901604fd:dXMtZWFzdC0yLmF3cy5lbGFzdGljLWNsb3VkLmNvbSQ3N2QxZDJiNGZjNWI0M2IxYmJiZjFmZDc1MzE1NmMyNyRhOTIyOWE3OWU1NTM0YjBlYTRmZTZlZjBlNjU1OTUxNQ==''',
  http_auth = ('enterprise_search','hylandforce1')
  ) """

  #clear the index(ces)
  #indices = [index]
  #es.delete_by_query(index=indices, body={"query": {"match_all": {}}})

  #print ("es info -> " + str(es.info()))

  """ data = [
    {
        "_index": "samplerekog",
        "doc" : {"name": "Rob","tag":"office"}
    },
    {
        "_index": "samplerekog",
        "doc" : {"name": "Rob","tag":"weapon"}
    },
    {
        "_index": "samplerekog",
        "doc" : {"name": "Rob","tag":"male"}
    },
    {
        "_index": "samplerekog",
        "doc" : {"name": "Jim","tag":"male"}
    },
] """
  newDoc = '''{{
            "_op_type":"{optype}",
            "index": "{indexpass}",
            "doc": [{doc}]
        }}'''.format(doc=docs,optype="index",indexpass=index)
  
  #print ('\ndocs info-> '+ newDoc)

  #print('\ncalling helpers bulk**')

  #print(json.loads(docs))
  #helpers.bulk(es, json.load(docs))
  #time.sleep(10)
   
if __name__ == "__main__":
    main()