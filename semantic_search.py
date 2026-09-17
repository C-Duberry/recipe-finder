from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

# MongoDB Atlas
atlas_client = MongoClient(os.getenv("MONGODB_URI"))
atlas_db = atlas_client["recipe_dataset"]
collection_atlas = atlas_db["recipes"]

# Load the saved FAISS index
index = faiss.read_index("output/recipe_index.faiss")

# Load the same Sentence Transformer model used to create the embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")



# Search for recipes that are semantically similar to the user's query
def semantic_search(query, k=4):

    # Create a list to store the matching recipes
    recipe_matches = []

    # Retrieve all recipes from MongoDB Atlas in the same order as their embeddings
    documents = list(collection_atlas.find())

    # Convert the user's query into an embedding
    query_embedding = model.encode(query)

    # Convert the query embedding into a NumPy array
    # FAISS expects float32 values
    query_embedding = np.array([query_embedding]).astype("float32")


    # Normalise the query embedding so it can be compared
    # using cosine similarity
    faiss.normalize_L2(query_embedding)

    # Search the FAISS index for the k closest recipe embeddings
    distances, indices = index.search(
        query_embedding,
        k=k
    )
    print(distances)
    print(indices)

    # Use the returned indices to find the matching recipes
    for i in indices[0]:
        recipe = documents[i]
        recipe_matches.append(recipe)

    # Return the matching recipes
    return recipe_matches



