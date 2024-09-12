import os
import sys
from mridumanda_shvedt.weather import get_weather, display_weather


def main():
    init()
    
    weather_data = get_weather()
    
    display_weather(weather_data)


def init():
    program_dir = os.path.join(os.getenv('HOME'), '.config', 'mridumanda')
    
    if not os.path.isfile(os.path.join(program_dir, 'api_key.txt')):
        os.makedirs(program_dir, exist_ok=True)
        
        api_key = input('Enter API key: ')
        
        with open(os.path.join(program_dir, 'api_key.txt'), 'w') as f:
            f.write(f"API={api_key}")
        
        print('API key saved successfully.')
        print('Run the program again, to use it.')
        
        sys.exit(0)