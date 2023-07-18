from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class UserTest(TestCase):

    def setUp(self):
        self.users = get_user_model().objects.all()
        self.username = 'testuser'
        self.username2 = 'testuser2'
        self.password = '12345'
        self.first_name = 'Jules'
        self.last_name = 'Verne'
        self.form_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
        }

    def test_create_user_db(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password,
                                                         first_name=self.first_name,
                                                         last_name=self.last_name)
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(all((
            self.users.first().first_name == self.first_name,
            self.users.first().last_name == self.last_name,
            self.users.first().username == self.username
        )))
        self.assertTrue(login)

    def test_create_user_form(self):
        response_register_user = self.client.post('/users/create/',
                                                  follow=True,
                                                  data=self.form_data)
        self.assertContains(response_register_user,
                            _('The user has been registered'),
                            status_code=200)
        self.assertTrue(all((
            self.users.first().first_name == self.first_name,
            self.users.first().last_name == self.last_name,
            self.users.first().username == self.username,
        )))
        self.assertEqual(self.users.count(), 1)

    def test_user_update_form(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password)
        self.client.login(username=self.username, password=self.password)
        response_update_user = self.client.post('/users/1/update/',
                                                follow=True,
                                                data=self.form_data)
        self.assertContains(response_update_user, _('The user has been updated'), status_code=200)
        self.assertTrue(all((
            self.users.first().first_name == self.first_name,
            self.users.first().last_name == self.last_name,
        )))

    def test_user_delete_form(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password)
        self.client.login(username=self.username, password=self.password)
        response_delete_user = self.client.post('/users/1/delete/',
                                                follow=True,
                                                data=self.form_data)

        self.assertContains(response_delete_user, _('The user has been deleted'), status_code=200)
        self.assertEqual(self.users.count(), 0)

    def test_login_right_form(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password)
        response_login_user = self.client.post('/login/',
                                               follow=True,
                                               data={
                                                   'username': self.username,
                                                   'password1': self.password,
                                               })
        self.assertContains(
            response_login_user,
            _('You have logged in'),
            status_code=200
        )

    def test_login_wrong_form(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password)
        response_login_user = self.client.post('/login/',
                                               follow=True,
                                               data={
                                                   'username': self.username2,
                                                   'password1': self.password,
                                               })
        self.assertContains(
            response_login_user,
            _('Enter correct username and password. Both fields can be case-sensitive'),
            status_code=200
        )
