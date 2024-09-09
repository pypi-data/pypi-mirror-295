from mridumanda_shvedt.weather import get_weather, display_weather

def main():
    weather_data = get_weather()
    
    display_weather(weather_data)