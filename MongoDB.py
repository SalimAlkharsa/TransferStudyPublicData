import json
import pymongo
import pandas as pd

def test_func():
  #Just a test func to see if colab clone worked
  print("Test successful!")
  pass

def upload_data_to_db(df, collection):
  password = input("Enter the db pw: ")
  client = pymongo.MongoClient("mongodb+srv://TransferDatabase:"+password+"@cluster0.pncv8.mongodb.net/test?retryWrites=true&w=majority")
  db = client.test
  db[collection].insert_many(df.to_dict('records'))
  pass

def read_db_to_df(collection, query ={}):
  password = input("Enter the db pw: ")
  client = pymongo.MongoClient("mongodb+srv://TransferDatabase:"+password+"@cluster0.pncv8.mongodb.net/test?retryWrites=true&w=majority")
  db = client.test
  cursor = db[collection].find({})
  df =  pd.DataFrame(cursor)
  return df
