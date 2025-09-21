import tkinter as tk
from tkinter import messagebox
import requests

weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    61: "Light rain",
    71: "Light snow",
    80: "Rain showers",
    95: "Thunderstorm",
}

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

def show_weather():
    city = city_entry.get()
    lat, lon, location_name = get_coordinates(city)

    if lat is None:
        messagebox.showerror("Error", "City not found.")
        return

    weather_data = get_weather(lat, lon)
    current = weather_data.get("current", {})

    temp = current.get("temperature_2m", '?')
    wind = current.get("wind_speed_10m", '?')
    code = current.get("weathercode", '?')
    condition = weather_codes.get(code, "Unknown")

    result_label.config(text=f"Weather in {location_name}:\n"
                             f"🌡️ Temp: {temp}°C\n"
                             f"💨 Wind: {wind} m/s\n"
                             f"🌥️ Condition: {condition}")

root = tk.Tk()
root.title("Weather App")
root.geometry("350x250")
root.resizable(False, False)

tk.Label(root, text="Enter city name:", font=("Arial", 12)).pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 12), width=30)
city_entry.pack()

get_button = tk.Button(root, text="Get Weather", command=show_weather, font=("Arial", 12))
get_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

root.mainloop()
