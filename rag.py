from openai import OpenAI
# from google import genai
import os
from dotenv import load_dotenv
from semantic_search import semantic_search

load_dotenv()

# client = genai.Client(
# api_key=os.getenv("GEMINI_API_KEY")
# )


client = OpenAI(
    api_key=os.getenv("OPENAI_ADMIN_KEY"),
    base_url="https://api.airforce/v1"
)


def generate_answer(query,recipes):

    # Create a piece of text for each recipe and join them together with a blank line
    context = "\n\n".join(
    f"""
    Recipe: {recipe["meal"]}
    Category: {recipe["category"]}
    Area: {recipe["area"]}
    Ingredients: {", ".join(recipe["ingredients"])}
    Instructions: {recipe["instructions"]}
    """
    for recipe in recipes
)

    # Create a prompt containing the user's query and retrieved recipes
    rag_prompt = f"""
    You are a friendly recipe assistant.
    Based on the user's query, recommend the most suitable recipes from the provided recipes.
    Keep the response friendly, conversational and helpful. Briefly explain why the recommendations suit the user's query.
    Keep your response under 80 words.
    Do not provide the full recipe, ingredients, area, category or instructions, as these will be displayed separately on the page.
    Do not use markup or markdown.
    Do not make recipe names bold.
    Do not use headings or write "Recipe:" before the recipe names.
    Only recommend recipes from the provided recipes.
    Do not ask any questions.


    Recipe information:
    {context}

    User's question:
    {query}
    """

    # Send the prompt to the LLM
    response =  client.chat.completions.create(
    model="llama-instant",
    messages=[{"role": "user", "content": rag_prompt}],
)

    #Return the LLM's answer
    return response.choices[0].message.content


