from pymongo import MongoClient
from config import Config
from dotenv import load_dotenv
load_dotenv()
import os

#client_connection = MongoClient('mongodb://localhost:27017')
client_connection = MongoClient(Config.DB_HOST, username='ca-data-admin', password=os.getenv('CA_DATA_ADMIN_PASSWORD'), authSource='ca-data', authMechanism='SCRAM-SHA-256')

client = client_connection['ca-data']

