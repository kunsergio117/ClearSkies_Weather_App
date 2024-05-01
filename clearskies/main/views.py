from django.shortcuts import render
import json
import urllib.request
from django.shortcuts import redirect
from django.urls import reverse

import json
import urllib.request
from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=638f32faed524313d58727ce950d0e20'
        url = urllib.parse.quote(url, safe=':/?&=')
        source = urllib.request.urlopen(url).read()
        list_of_data = json.loads(source)
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



