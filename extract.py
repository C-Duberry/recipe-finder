import requests
import string

# Loop through each letter of the alphabet to extract recipes
def return_data():
    all_recipes = []

    for letter in string.ascii_lowercase:
        response = requests.get(
            f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"
        )

        data = response.json()

        if data["meals"]:
            all_recipes.extend(data["meals"])

    return all_recipes
