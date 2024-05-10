import json
from django.shortcuts import render
import urllib.request
import urllib.parse
from .utils import calculate_feels_like  # Import the function to calculate feels like temperature
from pychartjs import ChartType, Color

API_KEY = '638f32faed524313d58727ce950d0e20'

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        # Get current weather data
        current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        current_url = urllib.parse.quote(current_url, safe=':/?&=')
        current_source = urllib.request.urlopen(current_url).read()
        current_data = json.loads(current_source)

        # Process current weather data
        temperature = float(current_data['main']['temp']) - 273.15  # Convert temperature to Celsius
        humidity = float(current_data['main']['humidity']) / 100.0  # Convert humidity to decimal
        wind_speed = float(current_data.get('wind', {}).get('speed', 0)) * 3.6  # Convert wind speed to km/h
        feels_like = calculate_feels_like(temperature, humidity, wind_speed)

        # Get forecast data for the next 5 days
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
        forecast_url = urllib.parse.quote(forecast_url, safe=':/?&=')
        forecast_source = urllib.request.urlopen(forecast_url).read()
        forecast_data = json.loads(forecast_source)

        # Process forecast data
        date_labels = []  # List to store date labels for x-axis
        temperature_values = []  # List to store temperature values for y-axis
        humidity_values = []  # List to store humidity values for y-axis
        for item in range(10):
            # Extract date, temperature, and humidity from forecast data
            date_labels.append(forecast_data['list'][item]['dt_txt'])  # Assuming 'dt_txt' contains date information
            temperature_values.append(float(forecast_data['list'][item]['main']['temp'] - 273.15))  # Convert temperature to Celsius
            humidity_values.append(float(forecast_data['list'][item]['main']['humidity'] / 100.0))  # Convert humidity to decimal

        # Create JSON data for temperature chart
        temperature_chart_data = {
            "labels": date_labels,
            "datasets": [{
                'label': 'Temperature (°C)',
                'data': temperature_values,
                'borderColor': Color.Red
            }]
        }
        temperature_chart_json = json.dumps(temperature_chart_data)

        # Create JSON data for humidity chart
        humidity_chart_data = {
            "labels": date_labels,
            "datasets": [{
                'label': 'Humidity (%)',
                'data': humidity_values,
                'borderColor': Color.Blue
            }]
        }
        humidity_chart_json = json.dumps(humidity_chart_data)

        data = {
            "temperature_chart_json": temperature_chart_json,
            "humidity_chart_json": humidity_chart_json,
            "feels_like": str(feels_like) + '°C'
        }
        # Debugging step: Print the data before passing it to the template
        print(data)
    else:
        data = {}
    return render(request, "main/index.html", data)
