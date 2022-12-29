import requests
from dotenv import load_dotenv
import os

load_dotenv(".env")

PRICES_ENDPOINT = os.getenv("PRICES_SHEET_ENDPOINT")
USER_ENDPOINT = os.getenv("USER_SHEET_ENDPOINT")


class DataManager:

    def __init__(self):
        self.data = None
        self.prices_sheet_data = []
        self.user_sheet_data = []
        self.get_sheet_data()
        self.get_user_sheet_data()

    def get_sheet_data(self):
        """Makes a request to the sheety api and returns all values on the prices sheet"""
        response = requests.get(url=PRICES_ENDPOINT)
        response.raise_for_status()
        self.prices_sheet_data = response.json()["prices"]

        return self.prices_sheet_data

    def update_sheet_data(self, iata_code, city):
        """Updates the sheet data if the IATA codes column isn't populated"""

        endpoint = f"{PRICES_ENDPOINT}/{city['id']}"
        params = {"price": {"iataCode": iata_code}
                  }

        response = requests.put(url=endpoint, json=params)
        response.raise_for_status()

        return response.text

    def get_user_sheet_data(self):
        """Makes a request to the Sheety API and returns all values on the users sheet"""
        response = requests.get(url=USER_ENDPOINT)
        response.raise_for_status()
        self.user_sheet_data = response.json()["users"]
        return self.user_sheet_data
