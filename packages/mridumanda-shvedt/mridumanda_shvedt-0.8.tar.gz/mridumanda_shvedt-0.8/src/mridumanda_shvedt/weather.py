import os, requests


def get_weather():
    city = input("Enter city: ")

    API_KEY = os.getenv('api_key')
    API_URL = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + API_KEY
    
    response = requests.get(API_URL)

    weather_data = response.json()

    temp = weather_data['main'].get('temp') - 273.15
    temp_min = weather_data['main'].get('temp_min') - 273.15
    temp_max = weather_data['main'].get('temp_max') - 273.15
    hum = weather_data['main'].get('humidity')
    desc = weather_data['weather'][0].get('description').title()
    city_name = weather_data['name']
    country = weather_data['sys'].get('country')
    location = f"Weather report for {city_name}, {country}"

    return [temp, temp_min, temp_max, hum, desc, location]


def display_weather(weather_data):
    os.system('clear')

    print(weather_data[-1])
    print(f" {'-' * (len(weather_data[-1]) - 2)} ")
    print(f"Temperature:          {weather_data[0]:.2f}")
    print(f"Humidity:             {weather_data[3]}")
    print(f"Min Temperature:      {weather_data[1]:.2f}")
    print(f"Max Temperature:      {weather_data[2]:.2f}")
    print(f"Condition:            {weather_data[4]}")