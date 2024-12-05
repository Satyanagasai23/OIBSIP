import requests

API_KEY = 'bd5e378503939ddaee76f12ad7a97608'  # Replace with your OpenWeatherMap API key

def fetch_weather_data(location):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = f"{base_url}appid={API_KEY}&q={location}"
    response = requests.get(complete_url)
    return response.json()

def display_weather_data(weather_data):
    if weather_data['cod'] != '404':
        main_data = weather_data['main']
        temperature = main_data['temp'] - 273.15  # Convert from Kelvin to Celsius
        humidity = main_data['humidity']
        weather_description = weather_data['weather'][0]['description']
        
        print(f"Temperature: {temperature:.2f}°C")
        print(f"Humidity: {humidity}%")
        print(f"Weather description: {weather_description.capitalize()}")
    else:
        print("City not found. Please try again.")

def main():
    location = input("Enter the city name or zip code: ")
    weather_data = fetch_weather_data(location)
    display_weather_data(weather_data)

if __name__ == "__main__":
    main()