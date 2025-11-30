import datetime
import requests
import string
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
load_dotenv()

GEOCODING_API_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
ONECALL_API_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"
api_key = os.getenv("OWM_API_KEY")
# api_key = os.environ.get("OWM_API_KEY")

app = Flask(__name__)


# Helper function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    """Convert Celsius temperature to Fahrenheit"""
    return round((celsius * 9/5) + 32)


# Display home page and get city name entered into search form
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form.get("search")
        print(f"User searched for city: {city}")
        return redirect(url_for("get_weather", city=city))
    print("Rendering home page")
    return render_template("index.html")


# Display weather forecast for specific city using data from OpenWeather API
@app.route("/<city>", methods=["GET", "POST"])
def get_weather(city):
    print(f"Fetching weather data for city: {city}")

    # Format city name and get current date to display on page
    city_name = string.capwords(city)
    print(f"Formatted city name: {city_name}")

    today = datetime.datetime.now()
    current_date = today.strftime("%A, %B %d")
    print(f"Current date: {current_date}")
    # Get latitude and longitude for city
    location_params = {
        "q": city_name,
        "appid": api_key,
        "limit": 3,
    }

    location_response = requests.get(GEOCODING_API_ENDPOINT, params=location_params)
    print(f"Geocoding API status code: {location_response.status_code}")
    location_data = location_response.json()
    print(f"Geocoding API raw response: {location_data}")

    # Prevent IndexError if user entered a city name with no coordinates by redirecting to error page
    if not location_data or not isinstance(location_data, list) or len(location_data) == 0:
        print(f"No coordinates found for city: {city_name}")
        print(f"Location API response: {location_data}")
        return redirect(url_for("error"))
    else:
        print(f"Location API response: {len(location_data)} results found")
        lat = location_data[0]['lat']
        lon = location_data[0]['lon']
        print(f"Coordinates - Lat: {lat}, Lon: {lon}")

    # Get all weather data from One Call API 3.0 (current + forecast in one call)
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
    }
    onecall_response = requests.get(ONECALL_API_ENDPOINT, weather_params)
    onecall_response.raise_for_status()
    onecall_data = onecall_response.json()

    # Verify required fields exist in API 3.0 response
    if 'current' not in onecall_data:
        print("Error: 'current' field missing from One Call API 3.0 response")
        return redirect(url_for("error"))

    if 'daily' not in onecall_data or len(onecall_data['daily']) < 5:
        print(f"Error: Insufficient forecast data from One Call API 3.0 (need 5 days, got {len(onecall_data.get('daily', []))})")
        return redirect(url_for("error"))

    # Extract current weather from 'current' object
    current_temp = round(onecall_data['current']['temp'])
    current_temp_f = celsius_to_fahrenheit(current_temp)
    current_weather = onecall_data['current']['weather'][0]['main']
    wind_speed = onecall_data['current']['wind_speed']

    # Extract today's min/max from 'daily[0]' (today's forecast)
    min_temp = round(onecall_data['daily'][0]['temp']['min'])
    min_temp_f = celsius_to_fahrenheit(min_temp)
    max_temp = round(onecall_data['daily'][0]['temp']['max'])
    max_temp_f = celsius_to_fahrenheit(max_temp)
    print(f"Current weather: {current_weather}, Temp: {current_temp}°C / {current_temp_f}°F, Min: {min_temp}°C / {min_temp_f}°F, Max: {max_temp}°C / {max_temp_f}°F, Wind: {wind_speed} m/s (from One Call API 3.0)")

    # Extract 5-day forecast from 'daily' array (indices 0-4 for 5 days)
    five_day_temp_list = [round(day['temp']['day']) for day in onecall_data['daily'][0:5]]
    five_day_temp_list_f = [celsius_to_fahrenheit(temp) for temp in five_day_temp_list]
    five_day_weather_list = [day['weather'][0]['main'] for day in onecall_data['daily'][0:5]]

    # Get next four weekdays to show user alongside weather data
    five_day_unformatted = [today, today + datetime.timedelta(days=1), today + datetime.timedelta(days=2),
                            today + datetime.timedelta(days=3), today + datetime.timedelta(days=4)]
    five_day_dates_list = [date.strftime("%a") for date in five_day_unformatted]
    print(f"5-day forecast prepared: {len(five_day_temp_list)} days (from One Call API 3.0 daily data)")
    print(f"Successfully fetched all weather data for {city_name} using One Call API 3.0")

    return render_template("city.html", city_name=city_name, current_date=current_date, current_temp=current_temp,
                           current_temp_f=current_temp_f, current_weather=current_weather, min_temp=min_temp,
                           min_temp_f=min_temp_f, max_temp=max_temp, max_temp_f=max_temp_f, wind_speed=wind_speed,
                           five_day_temp_list=five_day_temp_list, five_day_temp_list_f=five_day_temp_list_f,
                           five_day_weather_list=five_day_weather_list, five_day_dates_list=five_day_dates_list)


# Display error page for invalid input
@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
