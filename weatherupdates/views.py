from django.shortcuts import render
import requests
import json
from datetime import datetime

def index(request):
    try:
        if request.method == 'POST':
            API_KEY = 'put your API key here'
            city_name = request.POST.get('city')
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name},{state_code},{country_code}&appid={API_KEY}'
            response = requests.get(url).json()

            current_time = datetime.now()
            formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")

            city_weather_update = {
                'city': city_name,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'temperature': 'Temperature: ' + str(response['main']['temp']) + ' °C',
                'country_code': response['sys']['country'],
                'wind': 'Wind: ' + str(response['wind']['speed']) + 'km/h',
                'humidity': 'Humidity: ' + str(response['main']['humidity']) + '%',
                'time': formatted_time
            }

            # Adding your AccuWeather API integration here
            accuweather_url = "https://accuweatherstefan-skliarovv1.p.rapidapi.com/get24HoursConditionsByLocationKey"
            accuweather_payload = {"locationKey": "<REQUIRED>"}
            accuweather_headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": "dc9984440emsh05a772b6389862dp1c5578jsn2c34d484e148",
                "X-RapidAPI-Host": "AccuWeatherstefan-skliarovV1.p.rapidapi.com"
            }
            accuweather_response = requests.post(accuweather_url, data=accuweather_payload, headers=accuweather_headers).json()

            # Add the AccuWeather data to the existing dictionary
            city_weather_update['accuweather_data'] = accuweather_response

        else:
            city_weather_update = {}

        context = {'city_weather_update': city_weather_update}
        return render(request, 'weatherupdates/home.html', context)

    except:
        return render(request, 'weatherupdates/404.html')
