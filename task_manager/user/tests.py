from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.translation import gettext as _


class UserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self, **kwargs):
        self.users = get_user_model().objects.all()
        self.username, self.first_name, self.last_name = 'testuser', 'tester', 'testoff'
        self.password = 'qwe123qwe1'
        self.form_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
        }
        self.form_data_1 = {
            'id': self.users[0].id,
            'first_name': self.users[0].first_name,
            'last_name': self.users[0].last_name,
            'username': self.users[0].username,
            'password1': self.password,
            'password2': self.password,
        }
        self.form_data_2 = {
            'id': self.users[1].id,
            'first_name': self.users[1].first_name,
            'last_name': self.users[1].last_name,
            'username': self.users[1].username,
            'password1': self.password,
            'password2': self.password,
        }

    def test_create_user_form(self):
        response_register_user = self.client.post('/users/create/',
                                                  follow=True,
                                                  data=self.form_data)
        self.assertContains(response_register_user,
                            _('The user has been registered'),
                            status_code=200)

        self.assertIsNotNone(get_user_model().objects.filter(
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
        ))

    def test_create_unique_user_form(self):
        get_user_model().objects.create_user(first_name=self.first_name,
                                             last_name=self.last_name,
                                             username=self.username,
                                             password=self.password)

        response_register_user = self.client.post('/users/create/',
                                                  follow=True,
                                                  data=self.form_data)
        self.assertEqual(response_register_user.status_code, 200)
        self.assertIsNotNone(get_user_model().objects.filter(username=self.username))

    def test_user_update_form(self):
        self.client.login(username=self.form_data_1['username'],
                          password=self.form_data_1['password1'])
        response_update_user = self.client.post('/users/{}/update/'.format(self.form_data_1['id']),
                                                follow=True,
                                                data=self.form_data)
        self.assertContains(response_update_user, _('The user has been updated'), status_code=200)

        self.assertEqual(get_user_model().objects.get(
            id=self.form_data_1['id']).username, self.username)

    def test_user_delete_form(self):
        self.client.login(username=self.form_data_1['username'],
                          password=self.form_data_1['password1'])
        response_delete_user = self.client.post('/users/{}/delete/'.format(self.users[0].id),
                                                follow=True)
        self.assertContains(response_delete_user, _('The user has been deleted'), status_code=200)
        self.assertEqual(get_user_model().objects.filter(
            username=self.form_data_1['username']).exists(), False)

    def test_login_right_form(self):
        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password)
        response_login_user = self.client.post('/login/',
                                               follow=True,
                                               data={
                                                   'username': self.username,
                                                   'password': self.password,
                                               })
        self.assertContains(
            response_login_user,
            _('You have logged in'),
            status_code=200,
        )
        self.assertTrue(self.user.is_authenticated)

    def test_login_unexistent_user_form(self):
        response_login_user = self.client.post('/login/',
                                               data={
                                                   'username': self.username,
                                                   'password': self.password
                                               })
        self.assertContains(
            response_login_user,
            _('Enter correct username and password. Both fields can be case-sensitive'),
            status_code=200
        )

    def test_user_unauthorized(self):
        self.client.login(username=self.form_data_1['username'],
                          password=self.form_data_1['password1'])
        response_delete_user = self.client.post('/users/{}/delete/'.format(self.users[1].id),
                                                follow=True)
        self.assertContains(response_delete_user,
                            _('You are not authorized to change other users.'),
                            status_code=200)

        response_update_user = self.client.post('/users/{}/update/'.format(self.users[1].id),
                                                follow=True,
                                                data=self.form_data_2)
        self.assertContains(response_update_user,
                            _('You are not authorized to change other users.'),
                            status_code=200)
