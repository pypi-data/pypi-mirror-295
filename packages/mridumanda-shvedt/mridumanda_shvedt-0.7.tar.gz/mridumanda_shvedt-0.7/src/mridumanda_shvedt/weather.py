def main():
    import os, requests

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

    os.system('clear')

    print(location)
    print(f" {'-' * (len(location) - 2)} ")
    print(f"Temperature:          {temp:.2f}")
    print(f"Humidity:             {hum:.2f}")
    print(f"Min Temperature:      {temp_min:.2f}")
    print(f"Max Temperature:      {temp_max:.2f}")
    print(f"Condition:            {desc}")