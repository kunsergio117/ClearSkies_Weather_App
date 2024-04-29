from django.shortcuts import render
import json
import urllib.request
from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        city = request.POST['city']

        # Remove spaces from the URL and properly encode it
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=638f32faed524313d58727ce950d0e20'
        # Encode the URL to handle special characters
        url = urllib.parse.quote(url, safe=':/?&=')

        # Make the request to the API
        source = urllib.request.urlopen(url).read()

        # Convert JSON data to a dictionary
        list_of_data = json.loads(source)

        # Extract required data
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        print(data)
    else:
        data = {}
    return render(request, "main/index.html", data)
