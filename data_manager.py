import requests

SHEETY_PRICE_ENDPOINT = "https://api.sheety.co/b678785d551f6bcc64f76fbd962d4366/flightDeals/prices"
SHEETY_USER_ENDPOINT = "https://api.sheety.co/b678785d551f6bcc64f76fbd962d4366/flightDeals/users"


class DataManager:

    def __init__(self):
        self.sheety_data = {}

    # This class is responsible for talking to the Google Sheet.
    def get_codes(self):
        sheety_response = requests.get(url=SHEETY_PRICE_ENDPOINT)
        sheety_data = sheety_response.json()["prices"]
        return sheety_data

    def update_codes(self):
        for code in self.sheety_data:
            new_code = {
                "price": {
                    "iataCode": code["iataCode"]
                }
            }
            sheety_response = requests.put(url=f"{SHEETY_PRICE_ENDPOINT}/{code['id']}", json=new_code)
            print(sheety_response.text)

    def get_emails(self):
        sheety_response = requests.get(url=SHEETY_USER_ENDPOINT)
        sheety_data = sheety_response.json()["users"]
        print(sheety_data)
        return sheety_data

