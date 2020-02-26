from pymongo import MongoClient
from config import Config
import os

#client_connection = MongoClient('mongodb://localhost:27017')
client_connection = MongoClient(Config.DB_HOST, username='ca-data-admin', password='exabeam-ca-admin', authSource='ca-data', authMechanism='SCRAM-SHA-256')

client = client_connection['ca-data']
