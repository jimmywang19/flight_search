from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()
sheet_data = data_manager.get_destination_data()

ORIGIN_CITY_IATA = "LON"

for city in sheet_data:
    if city["iataCode"] == "":
        city["iataCode"] = flight_search.get_destination_code(city["city"])
data_manager.destination_data = sheet_data
data_manager.update()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=180)

for destination in data_manager.destination_data:
    flight_result = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        dst_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today)

    if flight_result and flight_result.price < destination["lowestPrice"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert! Only ${flight_result.price} to fly from {flight_result.origin_city}-" \
                  f"{flight_result.origin_airport} to" \
                  f" {flight_result.destination_city}-{flight_result.destination_airport}, " \
                  f"from {flight_result.out_date} to {flight_result.return_date}."

        if flight_result.stop_overs > 0:
            message += f"\nFlight has {flight_result.stop_overs} stop over, via {flight_result.via_city}."

        link = f"https://www.google.co.uk/flights?hl=en#flt={flight_result.origin_airport}." \
               f"{flight_result.destination_airport}.{flight_result.out_date}*{flight_result.destination_airport}." \
               f"{flight_result.origin_airport}.{flight_result.return_date}"

        notification_manager.send_msg(message)
        notification_manager.send_emails(emails, link, message)
