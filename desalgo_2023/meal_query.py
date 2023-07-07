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

query_content = input("Enter Meal: ")

query = {"query": query_content}


response = requests.request("POST", url, headers=headers, data=query)
food_dict = response.json()["foods"][0]


for key, value in food_dict.items():
    print("----------------------------------------")
    print(key, ":", value)
# for gui
