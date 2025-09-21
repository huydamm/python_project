import requests

def get_coordinates(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" in geo_data and len(geo_data["results"]) > 0:
        first_result = geo_data["results"][0]
        return first_result["latitude"], first_result["longitude"], first_result["name"]
    else:
        return None, None, None

def get_weather(lat, lon):
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current=temperature_2m,weathercode,wind_speed_10m"
    )
    weather_response = requests.get(weather_url)
    return weather_response.json()

# --- Main Program ---
city = input("Enter a city name: ")

lat, lon, location_name = get_coordinates(city)
if lat is None:
    print("City not found.")
else:
    weather_data = get_weather(lat, lon)
    current = weather_data.get("current", {})
    
    print(f"\nWeather in {location_name}:")
    print(f"Temperature: {current.get('temperature_2m', '?')}°C")
    print(f"Wind Speed: {current.get('wind_speed_10m', '?')} m/s")
    print(f"Weather Code: {current.get('weathercode', '?')}")
