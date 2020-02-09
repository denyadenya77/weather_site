from django.contrib.auth.models import User
from django.test import TestCase
from weather.models import UserCities


class TestUserCities(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('denys', 'myemail@test.com', 'denyadenya77')
        self.city = UserCities(user=self.user, city='london')

    def test_str(self):
        str_city = str(self.city)
        self.assertEqual(str_city, 'london')
