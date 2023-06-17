from django.test import TestCase
from django.contrib.auth import get_user_model


class StatusTest(TestCase):

    def setUp(self):
        self.users = get_user_model().objects.all()
        self.form_data = {
            'first_name': 'Jules',
            'last_name': 'Verne',
            'username': 'nemo',
            'password': '12345',
            'password_confirmation': '12345'
        }
