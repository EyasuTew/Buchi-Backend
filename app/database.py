import os

# import cloudinary
from dotenv import load_dotenv
from mongoengine import connect
from pymongo import MongoClient

load_dotenv()

# cloudinary.config(
#     api_key=os.environ.get('API_KEY'),
#     api_secret=os.environ.get('API_SECRET'),
#     cloud_name=os.environ.get('CLOUD_NAME'),
#     secure=True
# )

# database object
# connection = connect(
#     host=os.environ.get('MONGO_URL', 'mongodb://localhost:27017/buchi_db'),
#     us
#     uuidRepresentation='standard')
# 'mongodb://buchi_user:buchi_db@mongodb-1:27017/?retryWrites=true&w=majority'), uuidRepresentation='standard')

# connection = connect(host="localhost", port=27017,
#                       username="buchi_user",
#                       password="1234")
connection = ""

client = MongoClient("mongodb://root:example@localhost:27017/myproject?authSource=admin")
# host="localhost",
#                       username="some_user",
#                       password="random_pass",
#                       authSource='sample_db',
                      # authMechanism='SCRAM-SHA-256'
                      # )
print("Mongo")
print(client.__dict__)

                      # username="buchi_user",
                      # password="buchi1234")
# "mongodb+srv://buchi_user:1234@localhost:27017/?retryWrites=true&w=majority")

db = client.buchi_db

customer_collection = db["customers"]

pet_collection = db["pets"]

adoption_collection = db["adoptions"]