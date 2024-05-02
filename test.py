<<<<<<< Updated upstream
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
=======
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://jkl:Ii5ImtkQ06i754FV@cluster0.ev0dhqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
        print(e)
>>>>>>> Stashed changes
