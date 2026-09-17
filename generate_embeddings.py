from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

# Load the model used to convert recipe text into embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# MongoDB Atlas
atlas_client = MongoClient(os.getenv("MONGODB_URI"))
atlas_db = atlas_client["recipe_dataset"]
collection_atlas = atlas_db["recipes"]

document = collection_atlas.find_one()
print(document)

def embed_documents():
    # Create a list to hold all the updated documents
    updated_documents = []

    fields_to_embed = [
        "meal",
        "category",
        "area",
        "country",
        "ingredients",
        "instructions"
    ]

    # Go through each recipe in the collection
    for document in collection_atlas.find():

        # Create a temporary list to hold the fields we want to embed
        values = []

        # Get the value for each field we want to include
        for field in fields_to_embed:
            value = document[field]

            # Convert the ingredients list into a single string
            if field == "ingredients":
               value = ",".join(value)
            values.append(value)

        # Combine all the selected recipe information into one piece of text
        semantic_text = ",".join(values)

        # Convert the recipe text into an embedding
        document["embedding"] = model.encode(semantic_text).tolist()

        updated_documents.append(document)

    return updated_documents
