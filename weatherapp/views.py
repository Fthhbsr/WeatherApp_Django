from django.shortcuts import render, get_object_or_404, redirect
from decouple import config
import requests
# from pprint import pprint
from django.contrib import messages
from .models import City

def index(request):
    API_KEY = config("API_KEY")
    city = "Ankara"
    u_city = request.POST.get("name")
    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        # print(response.ok)

        if response.ok:
            content = response.json()
            r_city = content["name"]
            if City.objects.filter(name=r_city):
                messages.warning(request, "City already exists!")
            else:
                City.objects.create(name=r_city)

        else:
            messages.warning(request, "There is no city")


    city_data = []
    cities = City.objects.all()
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        content = response.json()
        data = {
            "city": city,
            "temp": content["main"]["temp"],
            "icon": content["weather"][0]["icon"],
            "desc": content["weather"][0]["description"]
        }
        city_data.append(data)
    # pprint(content)
  

    context = {
        "city_data": city_data
    }


    return render(request, 'weatherapp/index.html', context)


def delete_city(request, id):
    # city = City.objects.get(id=id)
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.warning(request, "City deleted.")
    return redirect("home")

# {'base': 'stations',
#  'clouds': {'all': 20},
#  'cod': 200,
#  'coord': {'lat': 39.9199, 'lon': 32.8543},
#  'dt': 1663090376,
#  'id': 323786,
#  'main': {'feels_like': 290.32,
#           'humidity': 48,
#           'pressure': 1010,
#           'temp': 291.21,
#           'temp_max': 291.81,
#           'temp_min': 289.9},
#  'name': 'Ankara',
#  'sys': {'country': 'TR',
#          'id': 267643,
#          'sunrise': 1663039649,
#          'sunset': 1663084921,
#          'type': 2},
#  'timezone': 10800,
#  'visibility': 10000,
#  'weather': [{'description': 'few clouds',
#               'icon': '02n',
#               'id': 801,
#               'main': 'Clouds'}],
#  'wind': {'deg': 330, 'speed': 8.23}}
