from pymongo import MongoClient
import os

#db= 'mongodb://localhost:27017' 
client_connection = MongoClient('mongodb://db:27017')

client = client_connection['testdatabase']


