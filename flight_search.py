import requests
from flight_data import FlightData
from pprint import pprint

TEQUILA_API_KEY = ""
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"


class FlightSearch:
    def find_code(self, city):
        print(city)
        headers = {
            "apikey": TEQUILA_API_KEY,
        }

        search_config = {
            "term": city,
            "location_types": "city",
        }

        tequila_response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=search_config, headers=headers)
        print(tequila_response)
        code = tequila_response.json()["locations"][0]["code"]
        print(code)
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
            headers = {
                "apikey": TEQUILA_API_KEY,
            }

            search_config = {
                "fly_from": origin_city_code,
                "fly_to": destination_city_code,
                "date_from": from_time.strftime("%d/%m/%Y"),
                "date_to": to_time.strftime("%d/%m/%Y"),
                "flight_type": "round",
                "one_for_city": 1,
                "max_stopovers": 0,
                "curr": "USD",
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 14,
            }

            tequila_response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=search_config,
                                            headers=headers)
            print(tequila_response)

            try:
                data = tequila_response.json()["data"][0]
            except IndexError:
                try:
                    search_config["max_stopovers"] = 1

                    tequila_response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=search_config,
                                                    headers=headers)

                    data = tequila_response.json()["data"][0]
                    print(data)

                except IndexError:
                    print(f"No flights found for {destination_city_code}.")
                    return None
                else:
                    flight_data = FlightData(
                        price=data["price"],
                        origin_city=data["route"][0]["cityFrom"],
                        origin_airport=data["route"][0]["flyFrom"],
                        destination_city=data["route"][1]["cityTo"],
                        destination_airport=data["route"][1]["flyTo"],
                        out_date=data["route"][0]["local_departure"].split("T")[0],
                        return_date=data["route"][1]["local_departure"].split("T")[0],
                        stop_overs=1,
                        via_city=data["route"][0]["cityTo"]
                    )

                    print(f"{flight_data.destination_city}: ${flight_data.price}")
                    return flight_data

            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][0]["cityTo"],
                    destination_airport=data["route"][0]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][1]["local_departure"].split("T")[0],
                )

                print(f"{flight_data.destination_city}: ${flight_data.price}")
                return flight_data


