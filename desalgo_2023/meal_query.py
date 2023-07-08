import requests
from dotenv import load_dotenv
import os


load_dotenv()

url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "x-app-id": os.getenv("api_id"),
    "x-app-key": os.getenv("api_key"),
    "x-remote-user-id": "0",
}


def search_meal(query_content, meals):
    query = {"query": query_content}

    response = requests.request("POST", url, headers=headers, data=query)
    food_dict = response.json()["foods"][0]

    name = food_dict["food_name"]
    grams = int(food_dict["serving_weight_grams"])

    calories = int(food_dict["nf_calories"])
    sugar = 0 if food_dict["nf_sugars"] is None else int(food_dict["nf_sugars"])
    saturated_fat = int(food_dict["nf_saturated_fat"])
    sodium = int(food_dict["nf_sodium"])
    fiber = (
        0
        if food_dict["nf_dietary_fiber"] is None
        else int(food_dict["nf_dietary_fiber"])
    )
    protein = int(food_dict["nf_protein"])

    meals[name] = {
        "grams": grams,
        "calories": calories,
        "sugar": sugar,
        "saturated_fat": saturated_fat,
        "sodium": sodium,
        "fiber": fiber,
        "protein": protein,
    }

    return meals
    # for key, value in food_dict.items():
    #     print("----------------------------------------")
    #     print(key, ":", value)
