from typing import Any
import os
import pandas as pd
from pymongo.mongo_client import MongoClient
import json
from ensure import ensure_annotations


class mongodb_operation:

     __collection = None
     __database = None

     def __init__(self, client_url:str, database_name:str, collection_name:str=None):
          self.client_url = client_url
          self.database_name = database_name
          self.collection_name = collection_name


     def create_client(self):
          return MongoClient(self.client_url)


     def create_database(self):
          if mongodb_operation.__database is None:
               client = self.create_client()
               mongodb_operation.__database = client[self.database_name]
          return mongodb_operation.__database


     def create_collection(self, collection_name: str =None):
          if mongodb_operation.__collection is None:
               database = self.create_database()
               if collection_name is not None:
                    mongodb_operation.__collection = database[collection_name]
               elif self.collection_name is not None:
                    mongodb_operation.__collection = database[self.collection_name]
               else:
                    raise ValueError("Collection name must be provided either during initialization or as an argument.")
          return mongodb_operation.__collection
         
               
     def insert_record(self, record:dict, collection_name:str):
          if isinstance(record, list):
               for data in record:
                    if not isinstance(data, dict):
                         raise TypeError("Record must be in the form of dict")
               
               collection = self.create_collection(collection_name)   
               collection.insert_many(record)  
          
          elif isinstance(record, dict):
               collection = self.create_collection(collection_name)
               collection.insert_one(record)
                    

     def bulk_insert(self, datafile:str, collection_name: str=None):
          self.path = datafile

          if self.path.endswith('.csv'):
               data = pd.read_csv(self.path, encoding='utf-8')

          elif self.path.endswith('.xlsx'):
               data = pd.read_excel(self.path, encoding='utf-8')

          datajson = json.loads(data.to_json(orient='record'))
          collection = self.create_collection(collection_name)
          collection.insert_many(datajson)