from django.urls import path
from .views import SearchPageView, search_result_view, city_weather_view, added_city_view, user_cities_view

urlpatterns = [
    path('', SearchPageView.as_view(), name='search_page'),
    path('search/', search_result_view, name='search_result_page'),
    path('city-weather/<str:cityname>', city_weather_view, name='city_weather_view'),
    path('added_city/<str:cityname>', added_city_view, name='added_city_view'),
    path('user_cities_view/', user_cities_view, name='user_cities_view'),
]