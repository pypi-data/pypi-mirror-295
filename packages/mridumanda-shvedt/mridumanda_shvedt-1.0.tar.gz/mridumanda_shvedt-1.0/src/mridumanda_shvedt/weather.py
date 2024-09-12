import os
import requests


def get_city_from_ip():
    try:
        ip_info_response = requests.get("https://ipinfo.io/json")
        
        if ip_info_response.status_code!= 200:
            raise Exception("Failed to get location from IP info \nEnter city name manually")
        
        return ip_info_response.json().get('city')
    
    except requests.exceptions.RequestException as e:
        print("Failed to get location from IP info \nEnter city name manually")
        return None


def get_weather():
    city = get_city_from_ip()
    
    if city == None:
        city = input("Enter city name: ")
    
    API_KEY = get_api_key()
    API_URL = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + API_KEY
    
    weather_map_response = requests.get(API_URL)

    weather_data = weather_map_response.json()

    temp = weather_data['main'].get('temp') - 273.15
    temp_min = weather_data['main'].get('temp_min') - 273.15
    temp_max = weather_data['main'].get('temp_max') - 273.15
    hum = weather_data['main'].get('humidity')
    pressure = weather_data['main'].get('pressure')
    desc = weather_data['weather'][0].get('description').title()
    city_name = weather_data['name']
    country = weather_data['sys'].get('country')
    location = f"Weather report for {city_name}, {country}"

    return [temp, temp_min, temp_max, hum, desc, pressure, location]


def get_api_key():
    api_key_file = os.path.join(os.getenv('HOME'), '.config','mridumanda', 'api_key.txt')

    with open(api_key_file, 'r') as f:
        api_key = f.read().split('=')[1].strip()

    return api_key


def display_weather(weather_data):
    os.system('clear')

    print(weather_data[-1])
    print(f" {'-' * (len(weather_data[-1]) - 2)} ")
    print(f"Temperature:          {weather_data[0]:.2f} °C")
    print(f"Humidity:             {weather_data[3]}%")
    print(f"Min Temperature:      {weather_data[1]:.2f} °C")
    print(f"Max Temperature:      {weather_data[2]:.2f} °C")
    print(f"Condition:            {weather_data[4]}")
    print(f"Pressure:             {weather_data[5]} hPa")