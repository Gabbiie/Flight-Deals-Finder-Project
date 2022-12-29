import requests
from dotenv import load_dotenv
import os

load_dotenv(".env")
ENDPOINT = os.getenv("USER_SHEET_ENDPOINT")

# Adds users to the flight club

print("Welcome to the FLight Club!\nWe find the best deals and email you.")
first_name = input("What is your first name?\n ").title()
last_name = input("What is your last name?\n ").title()
email = input("What is your email?\n ").lower()
retyped_email = input("Type your email again.\n ").lower()

if email == retyped_email:
    print("You\'re in the club!")
    parameters = {"user":
                      {"firstName": first_name,
                       "lastName": last_name,
                       "email": email
                       }}

    response = requests.post(url=ENDPOINT, json=parameters)
    response.raise_for_status()
    print(response.text)

else:
    print("The email address does not match.")
