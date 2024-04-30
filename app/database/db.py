from pymongo import MongoClient
from app.config import config

client = MongoClient(config.db_host)
db = client[config.db_name]