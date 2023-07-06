from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class UserTest(TestCase):

    def setUp(self):
        self.users = get_user_model().objects.all()
        self.username = 'testuser'
        self.password = '12345'
        self.form_data = {
            'first_name': 'Jules',
            'last_name': 'Verne',
            'username': self.username,
            'password': self.password,
            'password_confirmation': self.password
        }

    def test_user_read(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_create_user_db(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password)
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)

    def test_create_user_form(self):
        response_register_user = self.client.post('/users/create/',
                                                  follow=True,
                                                  data=self.form_data)
        self.assertContains(response_register_user,
                            _('The user has been registered'),
                            status_code=200)

        self.assertEqual(self.users.count(), 1)

    def test_user_update_form(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password)
        self.client.login(username=self.username, password=self.password)
        response_update_user = self.client.post('/users/1/update/',
                                                follow=True,
                                                data=self.form_data)
        self.assertContains(response_update_user, _('The user has been updated'), status_code=200)

    def test_user_delete_form(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password)
        self.client.login(username=self.username, password=self.password)
        response_delete_user = self.client.post('/users/1/delete/',
                                                follow=True,
                                                data=self.form_data)

        self.assertContains(response_delete_user, _('The user has been deleted'), status_code=200)
        self.assertEqual(self.users.count(), 0)
