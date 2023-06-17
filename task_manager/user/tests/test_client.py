from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTest(TestCase):

    def setUp(self):
        self.users = get_user_model().objects.all()
        self.form_data = {
            'first_name': 'Jules',
            'last_name': 'Verne',
            'username': 'nemo',
            'password': '12345',
            'password_confirmation': '12345'
        }

    def test_users_read(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_user_create_update_delete(self):
        self.assertEqual(self.users.count(), 0)
        # REGISTER
        response_register_user = self.client.post('/users/create/',
                                                  follow=True,
                                                  data=self.form_data)
        self.assertContains(response_register_user,
                            'The user has been registered',
                            status_code=200)

        self.assertEqual(self.users.count(), 1)
        # LOG IN
        self.client.post('/login/', follow=True, data={'username': self.form_data['username'],
                                                       'password': self.form_data['password']})
        # UPDATE
        response_update_user = self.client.post('/users/1/update/',
                                                follow=True,
                                                data=self.form_data)

        self.assertContains(response_update_user, 'The user has been updated', status_code=200)
        # DELETE
        response_delete_user = self.client.post('/users/1/delete/',
                                                follow=True,
                                                data=self.form_data)

        self.assertContains(response_delete_user, 'The user has been deleted', status_code=200)
        self.assertEqual(self.users.count(), 0)
