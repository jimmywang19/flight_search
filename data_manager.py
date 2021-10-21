import requests

SHEETY_PRICES_ENDPOINT = "YOUR_SHEETY_PRICES_ENDPOINT"
SHEETY_USERS_ENDPOINT = "YOUR_SHEETY_USERS_ENDPOINT"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        data = requests.get(url=SHEETY_PRICES_ENDPOINT).json()
        # print(data)
        self.destination_data = data["prices"]
        return self.destination_data

    def update(self):
        for city in self.destination_data:
            sheety_update_endpoint = f"{SHEETY_PRICES_ENDPOINT}/{city['id']}"
            sheety_params = {
                # We call the key price instead of prices due to Sheety being picky
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(url=sheety_update_endpoint, json=sheety_params)
            # print(response.text)

    def get_customer_emails(self):
        data = requests.get(url=SHEETY_USERS_ENDPOINT).json()
        self.customer_data = data["users"]
        return self.customer_data
