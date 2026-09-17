
import os
import faiss
import numpy as np
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

atlas_client = MongoClient(os.getenv("MONGODB_URI"))
atlas_db = atlas_client["recipe_dataset"]
collection_atlas = atlas_db["recipes"]

# Get embeddings from MongoDB Atlas
def get_embeddings():
    embeddings = []
    for document in collection_atlas.find():
        embeddings.append(document["embedding"])
    return embeddings


# create FAISS index
def create_faiss_index():

    # Get the embeddings and convert them into a NumPy array
    # FAISS expects the embeddings to be stored as float32
    embeddings = np.array(get_embeddings()).astype("float32")

    # Normalise the embeddings so that we can use cosine similarity
    faiss.normalize_L2(embeddings)

    # Find the number of dimensions in each embedding
    dimension = embeddings.shape[1]

    # Create a FAISS index using inner product
    # When the embeddings are normalised, inner product is equivalent to cosine similarity
    index = faiss.IndexFlatIP(dimension)

    # Add the embeddings to the index
    index.add(embeddings)

    return index

# Create FAISS index
index = create_faiss_index()


# Save the FAISS index so it can be loaded and reused later

def save_faiss_index(index):
    # Save the index to a file in the output folder
    faiss.write_index(index, "output/recipe_index.faiss")

save_faiss_index(index)