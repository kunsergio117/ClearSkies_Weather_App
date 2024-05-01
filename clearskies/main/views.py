from django.shortcuts import render
import json
import urllib.request
import urllib.parse
from .utils import calculate_feels_like  # Import the function to calculate feels like temperature
from pychartjs import BaseChart, ChartType, Color

API_KEY = '638f32faed524313d58727ce950d0e20'


class MyLineChart(BaseChart):
    type = ChartType.Line


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
        for item in range(5):
            # Extract date, temperature, and humidity from forecast data
            date_labels.append(forecast_data['list'][item]['dt_txt'])  # Assuming 'dt_txt' contains date information
            temperature_values.append(float(forecast_data['list'][item]['main']['temp'] - 273.15))  # Convert temperature to Celsius
            humidity_values.append(float(forecast_data['list'][item]['main']['humidity'] / 100.0))  # Convert humidity to decimal

        # Create line charts
        temperature_chart = MyLineChart()
        temperature_chart.data.labels = date_labels
        temperature_chart.data.datasets = [{
            'label': 'Temperature (°C)',
            'data': temperature_values,
            'borderColor': Color.Red
        }]

        humidity_chart = MyLineChart()
        humidity_chart.data.labels = date_labels
        humidity_chart.data.datasets = [{
            'label': 'Humidity (%)',
            'data': humidity_values,
            'borderColor': Color.Blue
        }]

        temperature_chart_json = temperature_chart.get()
        humidity_chart_json = humidity_chart.get()

        data = {
            "temperature_chart_json": temperature_chart_json,
            "humidity_chart_json": humidity_chart_json,
            "feels_like": str(feels_like) + '°C'
        }
        print(data)
    else:
        data = {}
    return render(request, "main/index.html", data)
