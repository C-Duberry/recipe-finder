import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Local MongoDB
local_client = MongoClient("mongodb://localhost:27017/")
local_db = local_client["recipe_dataset"]
collection_local = local_db["recipes"]

# MongoDB Atlas
atlas_client = MongoClient(os.getenv("MONGODB_URI"))
atlas_db = atlas_client["recipe_dataset"]
collection_atlas = atlas_db["recipes"]


def load_raw_data(data):
    collection_local.insert_many(data)


def get_raw_data():
    return list(collection_local.find())


def load_transformed_data(data):
    for document in data:
        document.pop("_id", None)

    collection_atlas.insert_many(data)

def load_embeddings(data):
    for document in data:
        collection_atlas.update_one(
            {"_id": document["_id"]},
            {"$set": {"embedding": document["embedding"]}}
        )
