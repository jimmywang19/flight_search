import requests
from datetime import datetime
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "YOUR_TEQUILA_API_KEY"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        query_param = {"term": city_name,}
        query_header = {"apikey": TEQUILA_API_KEY,}
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/locations/query",
            params=query_param,
            headers=query_header,
        )
        
        code = response.json()["locations"][0]["code"]
        return code

    def check_flights(self, origin_city_code, dst_city_code, from_time, to_time):
        flight_search_params = {
            "fly_from": origin_city_code,
            "fly_to": dst_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD",
        }
        flight_search_header = {"apikey": TEQUILA_API_KEY,}
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            params=flight_search_params,
            headers=flight_search_header
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {dst_city_code}.")
            print("Trying with stop overs set to 1")
            flight_search_params["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                params=flight_search_params,
                headers=flight_search_header
            )
            try:
                data = response.json()["data"][0]
                # print(data)
            except IndexError:
                print(f"Still no flights found for {dst_city_code}.")
                return None
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )

        print(f"{flight_data.destination_city}: ${flight_data.price}")
        return flight_data


