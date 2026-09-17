

from load import load_raw_data, load_transformed_data, get_raw_data, load_embeddings
from transform_data import transform_recipie_data
from extract import return_data
from generate_embeddings import embed_documents



# Return recipes from the API
# Loop through each letter of the alphabet to retrieve recipes for that letter

def main():

    # Extract data from API
    recipe_data = return_data()

    # Load raw data into MongoDB Compass
    load_raw_data(recipe_data)

    # Retrieve raw data from MongoDB Compass
    raw_data = get_raw_data()

    # Transform the raw data
    transformed_data = transform_recipie_data(raw_data)

    # Load transformed data into MongoDB Atlas
    load_transformed_data(transformed_data)

    # Create embeddings and load them into MongoDB Atlas
    load_embeddings(embed_documents())


main()
