from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
connection = ""

client = MongoClient("mongodb://root:example@mongo:27017/myproject?authSource=admin")

print("Mongo")
print(client.__dict__)

db = client.buchi_db

customer_collection = db["customers"]

pet_collection = db["pets"]

adoption_collection = db["adoptions"]