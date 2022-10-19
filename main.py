# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LHR"

data_manager = DataManager()
sheety_data = data_manager.get_codes()
email_data = data_manager.get_emails()

flight_search = FlightSearch()

notification_manager = NotificationManager()

# Check to see if the google sheet has iata codes; if not populate them
if not sheety_data[0]["iataCode"]:
    for code in sheety_data:
        flight_search = FlightSearch()
        # Set the new iata code to the one found from the search of the corresponding city
        code["iataCode"] = flight_search.find_code(code["city"])
    print(sheety_data)
    # Update the sheety_data in data_manager so that it has the updated list of iata codes
    data_manager.sheety_data = sheety_data
    # Update the google sheet with the new iata codes
    data_manager.update_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months = datetime.now() + timedelta(days=(6 * 30))

for destination in sheety_data:
    flight = flight_search.check_flights(ORIGIN_CITY_IATA, destination["iataCode"],
                                         from_time=tomorrow, to_time=six_months)
    if flight is not None and flight.price < destination["lowestPrice"]:
        print(flight.price)
        message = notification_manager.send_text(flight)
        notification_manager.send_emails(message, email_data)

# print(sheety_data)
