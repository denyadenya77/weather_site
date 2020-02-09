from django.test import TestCase
from .forms import UserRegisterForm

# Create your tests here.


class TestUserRegisterForm(TestCase):

    def test_user_registration_form_is_valid(self):
        form = UserRegisterForm(
            data={
                'username': 'denys',
                'email': 'jetropak7@gmail.com',
                'password1': 'denyadenya77',
                'password2': 'denyadenya77'
            }
        )

        self.assertTrue(form.is_valid())

    def test_user_registration_form_no_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
