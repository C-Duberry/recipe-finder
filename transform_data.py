from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["recipe_dataset"]
collection = db["recipes"]
collection_cleaned = db["recipies_cleaned"]



# Removes unnecessary fields from each recipe document.

# These fields are not needed for the project and removing them
# reduces unnecessary data and keeps the dataset focused.

def remove_fields(data):
    fields_to_remove = ["strMealAlternate",
                        "strImageSource",
                        "strCreativeCommonsConfirmed",
                        "dateModified",
                        "strTags"
                        ]
    for document in data:
           for key in fields_to_remove:
               document.pop(key, None)


# Renames fields in each recipe document to clearer and more
# consistent field names.

# The original API field names are long and inconsistent, so
# renaming them makes the data easier to understand and work with.

def update_field_names(data):
        for document in data:
            for key in list(document):
                if key.startswith("str"):
                    new_key = key[3:].lower()

                    document[new_key] = document.pop(key)


# Restructures the separate ingredient and measurement fields
# into a single ingredients array for each recipe.

# The original API stores ingredients and measurements in separate
# numbered fields. Combining them into strings such as "1 lb pork"
# creates a simpler, more readable structure that is easier to work with.
def restructure_ingredients(data):
    for document in data:
        # Create a list to store the ingredients and measurements for each recipe
        ingredients = []

        for i in range(1, 21):
            # Generate the field names for each ingredient and measurement
            measure_key = f"strMeasure{i}"
            ingredient_key = f"strIngredient{i}"

            # Retrieve the ingredient and measurement values
            measure = document[measure_key]
            ingredient = document[ingredient_key]

            # Add each non-empty ingredient and measurement as a single string
            if ingredient != "" and measure != "":
                ingredients.append(f"{measure} {ingredient}")

            # Remove the original separate ingredient and measurement fields
            del document[measure_key]
            del document[ingredient_key]

        # Add the new embedded ingredients array to the recipe document
        document["ingredients"] = ingredients


# Replaces NULL values with "Unknown" in the dataset.

# Missing values can make the data harder to work with, so
# replacing them with "Unknown" gives missing fields a consistent value.

def handle_null_values(data):

    for document in data:
        for key, value in document.items():
            if value is None or value == "":
                document[key] = "Unknown"


def transform_recipie_data(data):

    remove_fields(data)
    restructure_ingredients(data)
    update_field_names(data)
    handle_null_values(data)

    return data




