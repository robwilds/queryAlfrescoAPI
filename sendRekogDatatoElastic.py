# Import necessary libraries
import pandas as pd  # For data manipulation with DataFrames
from getpass import getpass  # For securely getting user input (passwords)
from elasticsearch import Elasticsearch, helpers  # For interacting with Elasticsearch
import os
from dotenv import load_dotenv

elasticID=os.getenv("elasticid")
elasticKey=os.getenv("elasticapikey")


def main(rekogDataFrame = None):
    # Read data from a CSV file into a DataFrame
    # The Repair Cafe International dataset can be downloaded at https://openrepair.org/open-data/downloads/
    #repair_data_df = pd.read_csv('/path/to/OpenRepairData_v0.3_RepairCafeInt_202309.csv')
    

    # Fill missing values in the DataFrame with 0
    #repair_data_df = repair_data_df.fillna(0)

    # Print the first few rows of the DataFrame to inspect the data

    # Create an Elasticsearch client using the provided credentials
    es = Elasticsearch(cloud_id=elasticID, api_key=elasticKey)

    # Define the name of the Elasticsearch index to be created
    index_name = 'RekogData'

    # Create the Elasticsearch index with the specified name
    es.indices.create(index=index_name)

    # Define a function to convert DataFrame rows to Elasticsearch documents
    def df_to_doc(df, name_of_index):
        for index, document in df.iterrows():
            yield dict(_index=name_of_index, _id=f"{document['id']}", _source=document.to_dict())

    # Use the Elasticsearch helpers.bulk() method to index the DataFrame data into Elasticsearch
    load = helpers.bulk(es, df_to_doc(repair_data_df, index_name))
    print(load)


if __name__ == "__main__":
    main()