import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client
from django.test import SimpleTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from . import views

# Create your tests here.


class SearchPageViewTest(SimpleTestCase):

    def test_search_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('search_page'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class SearchResultViewTest(SimpleTestCase):

    def test_search_page_status_code(self):
        response = self.client.get((reverse('search_result_page')))
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('search_result_page'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search_result_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')


class TestCityWeatherDetailView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_search_page_status_code(self):
        response = self.client.get(reverse('city_weather_class_based', kwargs={'cityname': 'london'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city_weater_class_based.html')


class TestFullCityWeatherDetailView(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        geckodriver_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'geckodriver'
        )

        options = Options()
        options.headless = True

        cls.selenium = webdriver.Firefox(options=options, executable_path=geckodriver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('denys')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('denyadenya77')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

    def test_search(self):
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        city_search_input = self.selenium.find_element_by_name("q")
        city_search_input.send_keys('london')

    def test_search_result_page(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/search/?q=london'))
        self.selenium.find_element_by_class_name('a').click()

    # def test_add_to_favourites(self):
    #     response = self.selenium.find_element_by_css_selector('#a').click()
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'city_added.html')










