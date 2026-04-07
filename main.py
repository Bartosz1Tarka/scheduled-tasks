# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

twilio_account_sid = os.getenv("TWILIO_SID")
twilio_auth_token = os.getenv("TWILIO_TOKEN")

#OPENWEATHERMAP

#wroclaw
#lon = 17.038538
#lat = 51.107883
lon = 23.045185
lat = 53.967057

owm_endpoint = "https://api.openweathermap.org/data/2.5/forecast?"
owm_api_key = os.getenv("OWM_API_KEY")

weather_params = {
    "lat": lat,
    "lon": lon,
    "appid": owm_api_key,
    "cnt": 4
}

response = requests.get(owm_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

#print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False

for item in weather_data["list"]:
    condition_code = item["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
    from_="whatsapp:+14155238886",
    body="It's going to rain today. Remember to bring an umbrella",
    to="whatsapp:+48534409400"
    )
    print("Bring an umbrella.")
    print(message.sid)
    message = client.messages(message.sid).fetch()
    print(message)
    print(message.error_code)
    print(message.error_message)
