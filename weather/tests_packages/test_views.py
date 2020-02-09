from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from weather.models import UserCities
from unittest.mock import patch


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('denys', 'myemail@test.com', 'denyadenya77')
        self.client = Client()
        self.client.login(username='denys', password='denyadenya77')

    def test_search_page_view(self):
        response = self.client.get(reverse('search_page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_search_result_view(self):
        response = self.client.get(reverse('search_result_page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')

    def test_city_weather_detail_view(self):
        response = self.client.get(reverse('city_weather_class_based', kwargs={'cityname': 'london'}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city_weater_class_based.html')
        self.assertEqual(response.context['city_in_favourites'], False)

    def test_added_city_view(self):
        response = self.client.get(reverse('added_city_view', kwargs={'cityname': 'london'}))

        cities = self.user.usercities_set.all()
        city_in_favourites = cities.filter(city__iexact='london').exists()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city_added.html')
        self.assertEqual(response.context['city'], 'london')
        self.assertEqual(city_in_favourites, True)

    @patch('weather.get_weather.Weather.get_current_weather')
    def test_user_cities_view(self, mock_get_current_weather):
        mock_get_current_weather.return_value = {"name": "london"}

        UserCities.objects.create(user=self.user, city='london')
        response = self.client.get(reverse('user_cities_view'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_cities_view.html')
        self.assertEqual(response.context['name'], 'london')

    @patch('weather.get_weather.Weather.get_current_weather')
    def test_user_cities_view_apierror(self, mock_get_current_weather):
        mock_get_current_weather.return_value = {"error": "APIError"}
        response = self.client.get(reverse('user_cities_view'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_cities_view.html')
        self.assertEqual(response.context['error'], 'APIError')

    def test_delete_city_view(self):
        UserCities.objects.create(user=self.user, city='london')

        response = self.client.get(reverse('delete_city_view', kwargs={'cityname': 'london'}))

        cities = self.user.usercities_set.all()
        city_in_favourites = cities.filter(city__iexact='london').exists()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city_deleted.html')
        self.assertEqual(city_in_favourites, False)
