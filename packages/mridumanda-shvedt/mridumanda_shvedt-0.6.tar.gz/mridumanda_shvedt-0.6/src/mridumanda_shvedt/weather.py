def main():
    import os, requests

    city = input("Enter city: ")

    API_KEY = os.getenv('api_key')
    API_URL = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + API_KEY

    response = requests.get(API_URL)

    weather_data = response.json()

    cityName = weather_data['name']
    temp = weather_data['main'].get('temp') - 273.15
    temp_min = weather_data['main'].get('temp_min') - 273.15
    temp_max = weather_data['main'].get('temp_max') - 273.15
    hum = weather_data['main'].get('humidity')
    desc = weather_data['weather'][0].get('description').title()
    city_name = weather_data['name']
    country = weather_data['sys'].get('country')

    print(f"Weather report for {cityName}, {country}")
    print("-----------------------------------")
    print("Temperature:         ", temp)
    print("Humidity:            ", hum)
    print("Min Temperature:     ", temp_min)
    print("Max Temperature:     ", temp_max)
    print("Condition:           ", desc)