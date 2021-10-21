Flight Search is a program that notifies you and your users when a flight's cost is cheaper than the Lowest Price you set. See images below.
You will receive a text notification while your users receive an email notification.

## How to use?
1. Setup a Twilio account and modify the notification_manager.py. Fill in all info required.
2. Setup a Sheety account and modify the data_manager.py to insert your endpoints
   - Note, you will need to create a Google Sheet with 2 tabs: "prices" and "users". See images below.
   - Note, you can leave the users Google Sheet empty if you only intend to use this for yourself.
3. Setup a Tequila account and modify the flight_search.py to insert your Tequila API key
4. In main.py, modify the ORIGIN_CITY_IATA and set it to your city's IATA.

Note, you can only make up to 200 requests per month on the free Sheety account. Upgrade your account for more requests.
![prices](https://user-images.githubusercontent.com/24804326/138363840-817a682d-941e-440e-87a3-37cced2a94c4.png)
![users](https://user-images.githubusercontent.com/24804326/138363849-f86e9a30-ecd7-4760-aa94-b3cb8546d63f.png)
