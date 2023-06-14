from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTest(TestCase):

    def setUp(self):
        self.username = 'nemo',
        self.password = '12345',
        self.first_name = 'Jules',
        self.last_name = 'Verne'

    def test_users_get(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/users.html')

    def test_register_get(self):
        response = self.client.get('/users/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/new_user.html')

    def test_user_register_and_delete_post(self):
        response_register = self.client.post('/users/create/', data={
            'first_name': self.first_name,
            'last_name': self.first_name,
            'username': self.username,
            'password': self.password,
            'password_confirmation': self.password
        })
        self.assertEqual(response_register.status_code, 302)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
