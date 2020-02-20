from pymongo import MongoClient
import os

db= 'mongodb://localhost:27017' 
client_connection = MongoClient(db)	#os.environ('DB_PORT_27017_TCP_PROTO', 27017) replace db with the env variable.
client = client_connection['testdatase']
