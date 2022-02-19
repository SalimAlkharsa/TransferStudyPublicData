import json
import pymongo
import pandas as pd

def test_func():
  #Just a test func to see if colab clone worked
  print("Test successful!")
  pass

def upload_data_to_db(file, BASE):
  password = input("Enter the db pw: ")
  client = pymongo.MongoClient("mongodb+srv://TransferDatabase:"+password+"@cluster0.pncv8.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", connect=False)
  db = client.test
  df = pd.read_csv(file+'.csv',encoding = 'ISO-8859-1')   # loading csv file
  df.to_json('yourjson.json')                               # saving to json file
  jdf = open('yourjson.json').read()                        # loading the json file 
  data = json.loads(jdf)
  db[BASE].insert_many([data])
  pass
