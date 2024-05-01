from django.shortcuts import render
import json
import urllib.request
import urllib.parse
from .utils import calculate_feels_like  # Import the function to calculate feels like temperature

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=638f32faed524313d58727ce950d0e20'
        url = urllib.parse.quote(url, safe=':/?&=')
        source = urllib.request.urlopen(url).read()
        list_of_data = json.loads(source)
        temperature = float(list_of_data['main']['temp']) - 273.15  # Convert temperature to Celsius
        humidity = float(list_of_data['main']['humidity']) / 100.0  # Convert humidity to decimal
        wind_speed = float(list_of_data.get('wind', {}).get('speed', 0)) * 3.6  # Convert wind speed to km/h
        feels_like = calculate_feels_like(temperature, humidity, wind_speed)
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
            "temp": str(temperature) + '°C',
            "feels_like": str(feels_like) + '°C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        print(data)
    else:
        data = {}
    return render(request, "main/index.html", data)
