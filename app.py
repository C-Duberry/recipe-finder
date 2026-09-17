
from flask import Flask, request, render_template
from rag import generate_answer
from semantic_search import semantic_search
import re


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    # Get the user's search query from the form
    query = request.form["query"]

    # Find recipes that are semantically similar to the query
    recipes = semantic_search(query)

    # Split the instructions into separate steps after each sentence
    for recipe in recipes:
        instructions = re.sub(
            r'\bstep\s+\d+\b',
            '',
            recipe["instructions"],
            flags=re.IGNORECASE
        )

        # Split the instructions using line breaks and remove empty steps
        recipe["steps"] = [
            step
            for step in re.split(r'\r\n', instructions)
            if step
        ]

    try:
        # Generate an answer using the retrieved recipes and Gemini
        answer = generate_answer(query, recipes)

        # Display the answer and recipes on the webpage
        return render_template(
            "index.html",
            answer=answer,
            recipes=recipes
        )

    except Exception as e:
        print(e)

        # Display the recipes if the LLM fails
        return render_template(
            "index.html",
            answer=None,
            recipes=recipes
        )

if __name__ == "__main__":
    app.run(debug=True)