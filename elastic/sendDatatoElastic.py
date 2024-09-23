# Import necessary libraries
import pandas as pd  # For data manipulation with DataFrames
from elasticsearch import Elasticsearch
import configparser

config = configparser.ConfigParser()
config.read('elastic.ini')

def main(elasticData = None,index=None,document=None):

    # Create an Elasticsearch client using the provided credentials
    #es = Elasticsearch(cloud_id=elasticID, api_key=elasticKey) #use this for api key access
    es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password']))

    print ("es info -> " + str(es.info()))

    #clear the index(ces)
    indices = ['lord-of-the-rings']
    es.delete_by_query(index=indices, body={"query": {"match_all": {}}})

    #now index some data
    es.index(refresh='true',
 index='lord-of-the-rings',
 document={
  'character': 'Aragon',
  'quote': 'It is not this day.'
 })
    
    es.index(refresh='true',
 index='lord-of-the-rings',
 document={
  'character': 'Gandalf',
  'quote': 'A wizard is never late, nor is he early.'
 })
    
    es.index(refresh='true',
 index='lord-of-the-rings',
 document={
  'character': 'Frodo Baggins',
  'quote': 'You are late'
 })

if __name__ == "__main__":
    main()