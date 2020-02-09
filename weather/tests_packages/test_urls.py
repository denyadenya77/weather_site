from django.test import SimpleTestCase
from django.urls import reverse, resolve
from weather import views


class TestUrls(SimpleTestCase):

    def test_search_url_resolves(self):
        url = reverse('search_page')
        response = resolve(url)
        self.assertEqual(response.func.view_class, views.SearchPageView)

    def test_search_result_page_resolves(self):
        url = reverse('search_result_page')
        response = resolve(url)
        self.assertEqual(response.func.view_class, views.SearchResultView)

    def test_city_weather_class_based_resolves(self):
        url = reverse('city_weather_class_based', kwargs={'cityname': 'london'})
        response = resolve(url)
        self.assertEqual(response.func.view_class, views.CityWeatherDetailView)

    def test_user_cities_view_resolves(self):
        url = reverse('user_cities_view')
        response = resolve(url)
        self.assertEqual(response.func.view_class, views.UserCitiesView)


    def test_added_city_view_resolves(self):
        url = reverse('added_city_view', kwargs={'cityname': 'london'})
        response = resolve(url)
        self.assertEqual(response.func.view_class, views.AddedCityView)
    

    def test_delete_city_view_resolves(self):
        url = reverse('delete_city_view', kwargs={'cityname': 'london'})
        response = resolve(url)
        self.assertEqual(response.func.view_class, views.DeleteCityView)




