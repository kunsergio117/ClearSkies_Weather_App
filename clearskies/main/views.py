import json
from django.shortcuts import render
import urllib.request
import urllib.parse
from .utils import calculate_feels_like  # Import the function to calculate feels like temperature
from pychartjs import ChartType, Color

API_KEY = '638f32faed524313d58727ce950d0e20'

# Functions to convert temperature units
def convert_to_imperial(celsius):
    return (celsius * 9/5) + 32

def convert_to_metric(fahrenheit):
    return (fahrenheit - 32) * (5/9)

def index(request):
    if request.method == 'POST':
        unit = request.POST.get('unit', 'metric')  # Get the selected unit option, defaulting to metric
        city = request.POST['city']

        current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        current_url = urllib.parse.quote(current_url, safe=':/?&=')
        current_source = urllib.request.urlopen(current_url).read()
        current_data = json.loads(current_source)

        temperature = float(current_data['main']['temp']) - 273.15  # Convert temperature to Celsius
        humidity = float(current_data['main']['humidity']) / 100.0  # Convert humidity to decimal
        wind_speed = float(current_data.get('wind', {}).get('speed', 0)) * 3.6  # Convert wind speed to km/h
        feels_like = calculate_feels_like(temperature, humidity, wind_speed)

        # Temperature unit conversion based on user selection
        if unit == 'imperial':
            temperature = convert_to_imperial(temperature)
            feels_like = convert_to_imperial(feels_like)
            temp_unit = '°F'
        else:
            temp_unit = '°C'

        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
        forecast_url = urllib.parse.quote(forecast_url, safe=':/?&=')
        forecast_source = urllib.request.urlopen(forecast_url).read()
        forecast_data = json.loads(forecast_source)

        date_labels = []
        temperature_values = []
        humidity_values = []
        for item in range(10):
            date_labels.append(forecast_data['list'][item]['dt_txt'])
            temp_val = float(forecast_data['list'][item]['main']['temp']) - 273.15
            if unit == 'imperial':
                temp_val = convert_to_imperial(temp_val)
            temperature_values.append(temp_val)
            humidity_values.append(float(forecast_data['list'][item]['main']['humidity']) / 100.0)


        # Convert temperature values to Fahrenheit if the selected unit is imperial
        if unit == 'imperial':
            temperature_values_fahrenheit = [convert_to_imperial(temp_val) for temp_val in temperature_values]
        else:
            temperature_values_fahrenheit = temperature_values  # Keep the data as Celsius if metric

        # Temperature chart data for Celsius
        temperature_chart_data_celsius = {
            'labels': date_labels,
            'datasets': [{
                'label': 'Temperature (°C)',
                'data': temperature_values,
                'borderColor': 'rgba(75, 192, 192, 1)'
            }]
        }

        # Temperature chart data for Fahrenheit
        temperature_chart_data_fahrenheit = {
            'labels': date_labels,
            'datasets': [{
                'label': 'Temperature (°F)',
                'data': temperature_values_fahrenheit,
                'borderColor': 'rgba(255, 99, 132, 1)'
            }]
        }


        humidity_chart_data = {
            'labels': date_labels,
            'datasets': [{
                'label': 'Humidity (%)',
                'data': humidity_values,
                'borderColor': Color.Blue
            }]
        }

        temperature_chart_json_celsius = json.dumps(temperature_chart_data_celsius)
        temperature_chart_json_fahrenheit = json.dumps(temperature_chart_data_fahrenheit)
        humidity_chart_json = json.dumps(humidity_chart_data)

        data = {
            'temperature_chart_json_celsius': temperature_chart_json_celsius,
            'temperature_chart_json_fahrenheit': temperature_chart_json_fahrenheit,
            'humidity_chart_json': humidity_chart_json,
            'feels_like': f'{feels_like:.2f}{temp_unit}'
        }
    else:
        data = {}
    return render(request, 'main/index.html', data)
