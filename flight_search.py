from datetime import datetime, timedelta
import requests
from flight_data import FlightData
from dotenv import load_dotenv
import os

load_dotenv(".env")
API_KEY = os.getenv("KIWI_API_KEY")

MIN_DURATION = 7
MAX_DURATION = 28
CURRENCY = "GBP"
ORIGIN_CITY_CODE = "LTN"

ENDPOINT = "https://api.tequila.kiwi.com"


class FlightSearch:

    def get_iata_code(self, city):
        """"Get IATA code for each city on the sheet"""

        header = {"apikey": API_KEY}
        params = {"term": city,
                  "locale": "en-US",
                  "location_types": "airport",
                  "active_only": "true"}

        response = requests.get(url=f"{ENDPOINT}/locations/query", params=params, headers=header)
        response.raise_for_status()
        print(response.text)
        airport_code = response.json()["locations"][0]["city"]["code"]

        return airport_code

    def check_flight(self, city_code, city_name):
        """"Check if there is any flight available from the origin city to the potential destination cities"""

        headers = {"apikey": API_KEY}

        # Checks for available flights in the next 6 months.
        tomorrow = datetime.now() + timedelta(days=1)
        in_6_months_time = tomorrow + timedelta(days=6*30)

        parameters = {
                      "fly_from": ORIGIN_CITY_CODE,
                      "fly_to": city_code,
                      "date_from": tomorrow.strftime("%d/%m/%Y"),
                      "date_to": in_6_months_time.strftime("%d/%m/%Y"),
                      "nights_in_dst_from": MIN_DURATION,
                      "nights_in_dst_to": MAX_DURATION,
                      "flight_type": "round",
                      "max_stopovers": 0,
                      "one_for_city": 1,
                      "curr": CURRENCY}

        response = requests.get(url=f"{ENDPOINT}/v2/search", params=parameters, headers=headers)
        response.raise_for_status()

        try:
            # Checks for a direct flight
            data = response.json()["data"][0]

        except IndexError:
            # If a direct flight isn't available, check for connecting flights.
            parameters["max_stopovers"] = 1

            response = requests.get(url=f"{ENDPOINT}/v2/search", params=parameters, headers=headers)
            response.raise_for_status()

            try:
                # If a connecting flight isn't available then give feedback
                data = response.json()["data"][0]
            except IndexError:
                print(f"No available flights to {city_name}.")
                return None
            else:
                flight_data = FlightData(
                    origin_city=data["route"][0]["cityFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    origin_code=data["route"][0]["flyFrom"],
                    destination_code=data["route"][1]["flyTo"],
                    price=data["price"],
                    departure_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"])
                return flight_data
        else:
            flight_info = FlightData(origin_city=data["route"][0]["cityFrom"],
                                     origin_code=data["route"][0]["cityCodeFrom"],
                                     destination_city=data["route"][0]["cityTo"],
                                     destination_code=data["route"][0]["cityCodeTo"],
                                     price=data["price"],
                                     departure_date=data["route"][0]["local_departure"].split("T")[0],
                                     return_date=data["route"][1]["local_departure"].split("T")[0],
                                     )
            print(f"{flight_info.destination_city}: {flight_info.price}")

            return flight_info
