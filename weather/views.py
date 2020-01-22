from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import UserCities

# Create your views here.


class SearchPageView(TemplateView):
    template_name = 'home.html'


def search_result_view(request):
    city_name = request.GET.get('q')
    return render(request, 'search_results.html', {'city_name': city_name})


def city_weather_view(request, cityname):
    city = cityname
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=4b0474b68bb0012daed655d182e69e2a&units=metric'
    res = requests.get(url)
    weather = res.json()

    # get today's date
    now = datetime.now()
    dt_string = now.strftime("%d")
    date_to_view = str(now)[:10]

    five_days_list = weather['list']

    # air temperature for today
    current_weather = weather['list'][0]['main']['temp']

    weather_ready = []

    for day in five_days_list:

        date = day['dt_txt'][8:10]
        time = day['dt_txt'][11:13]

        if time == '12' and date != dt_string:
            day['dt_txt'] = day['dt_txt'][:10]
            weather_ready.append(day)

    context = {
        'city': city,
        'today_day': date_to_view,
        'today_temp': current_weather,
        'weather_ready': weather_ready,
    }

    return render(request, 'city_weather.html', context=context)

@login_required
def added_city_view(request, cityname):
    city = cityname
    current_user = request.user

    city_to_db = UserCities(user=current_user, city=city)
    city_to_db.save()

    context = {
        'city': city
    }
    return render(request, 'city_added.html', context=context)


@login_required
def user_cities_view(request):
    current_user = request.user

    user_cities_list = UserCities.objects.filter(user=current_user)

    context = {
        'city_list': []
    }

    for city in user_cities_list:

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=4b0474b68bb0012daed655d182e69e2a&units=metric'
        res = requests.get(url)
        weather = res.json()

        city_dict = {
            'name': weather['name'],
            'temp': weather['main']['temp']
        }

        context['city_list'].append(city_dict)

    return render(request, 'user_cities_view.html', context=context)

