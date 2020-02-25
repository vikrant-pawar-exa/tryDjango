from pymongo import MongoClient
from config import Config
import os

#client_connection = MongoClient('mongodb://localhost:27017')
client_connection = MongoClient(Config.DB_HOST)

client = client_connection['testdatabase']


