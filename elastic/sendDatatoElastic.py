# Import necessary libraries
import pandas as pd  # For data manipulation with DataFrames
#from getpass import getpass  # For securely getting user input (passwords)
from elasticsearch import Elasticsearch, helpers
import configparser
import os
from dotenv import load_dotenv

elasticCloudID=os.getenv("elasticcloudid")
elasticKey=os.getenv("elasticapikey")
elasticUser = os.getenv("elasticuser")
elasticPassword = os.getenv("elasticpassword")

config = configparser.ConfigParser()
config.read('elastic.ini')

def main(elasticData = None,index=None,document=None):
    # Read data from a CSV file into a DataFrame
    # The Repair Cafe International dataset can be downloaded at https://openrepair.org/open-data/downloads/
    #repair_data_df = pd.read_csv('/path/to/OpenRepairData_v0.3_RepairCafeInt_202309.csv')

    # Create an Elasticsearch client using the provided credentials
    #es = Elasticsearch(cloud_id=elasticID, api_key=elasticKey)
    es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password']))

    print ("es info -> " + str(es.info()))

    #now index some data
    es.index(
 index='lord-of-the-rings',
 document={
  'character': 'Aragon',
  'quote': 'It is not this day.'
 })
    
    es.index(
 index='lord-of-the-rings',
 document={
  'character': 'Gandalf',
  'quote': 'A wizard is never late, nor is he early.'
 })
    
    es.index(
 index='lord-of-the-rings',
 document={
  'character': 'Frodo Baggins',
  'quote': 'You are late'
 })

if __name__ == "__main__":
    main()