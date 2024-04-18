import requests

api_key = ""
city = "Mumbai"
url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

response = requests.get(url)

if response.status_code == 200:
    weather_data = response.json()
    if 'current' in weather_data and 'condition' in weather_data['current'] and 'temp_c' in weather_data['current']:
        description = weather_data['current']['condition']['text']
        temperature = weather_data['current']['temp_c']
        print(f"Weather in {city}: {description}, Temperature: {temperature}°C")
    else:
        print("Error: Weather data format unexpected")
else:
    print(f"Error {response.status_code} while fetching weather data")
