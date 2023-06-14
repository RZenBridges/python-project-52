from django.test import TestCase
from task_manager.user.models import User
from django.contrib.auth import login


class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='nemo',
            password='qwerty',
            first_name='Jules',
            last_name='Verne'
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = login(username='nemo', password='qwerty')
        self.assertTrue((user is not None) and user.is_authenticated)
