from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Get all the data from both sheets
prices_data = data_manager.prices_sheet_data
user_data = data_manager.user_sheet_data

# If the iata code column isn't populated, get the codes from tequila and write them onto the sheet
if any(entry["iataCode"] == "" for entry in prices_data):
    for destination in prices_data:
        code = flight_search.get_iata_code(destination["city"])
        destination["iataCode"] = code
        print(data_manager.update_sheet_data(code, destination))

# For each city listed on the sheet, check for available flights and send the relevant information via a sms
# and email the info to each client/user listed on the users sheet.
flight = None

for row in prices_data:
    if row["id"] >= 2:
        flight = flight_search.check_flight(city_code=row["iataCode"], city_name=row["city"])

    # Send emails and sms if there is a low price
    if flight:
        if flight.price <= row["lowestPrice"]:

            text = f"Low price Alert! Only £{flight.price} to fly from {flight.origin_city}" \
                       f"-{flight.origin_code} to {flight.destination_city}-{flight.destination_code}" \
                       f" from {flight.departure_date} to {flight.return_date}." \
                       f"\nhttps://www.google.co.uk/flights?hl=en#flt={flight.origin_code}.{flight.destination_code}" \
                       f".{flight.departure_date}*{flight.destination_code}.{flight.origin_code}.{flight.return_date}"

            if flight.stop_overs > 0:
                text += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

            print(notification_manager.send_text(text))
            print(text)

            emails = [row["email"] for row in user_data]
            print(emails)

            notification_manager.send_emails(message=text.encode('utf-8'), emails_list=emails)
