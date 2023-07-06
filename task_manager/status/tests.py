from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Status
from django.utils.translation import gettext as _


class StatusTest(TestCase):

    def setUp(self):
        self.statuses = Status.objects.all()
        self.username = 'testuser'
        self.password = '12345'
        self.status = 'test_status'
        get_user_model().objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_status_read(self):
        response = self.client.get('/statuses/')
        self.assertEqual(response.status_code, 200)

    def test_create_status_db(self):
        Status.objects.create(name=self.status)
        self.assertEqual(self.statuses.count(), 1)

    def test_create_status_form(self):
        response_create_status = self.client.post('/statuses/create/',
                                                  follow=True,
                                                  data={'name': self.status})
        self.assertContains(response_create_status,
                            _('The status has been created'),
                            status_code=200)
        self.assertEqual(self.statuses.count(), 1)

    def test_update_status_form(self):
        Status.objects.create(name=self.status)
        response_update_status = self.client.post('/statuses/1/update/',
                                                  follow=True,
                                                  data={'name': self.status})
        self.assertContains(response_update_status,
                            _('The status has been updated'),
                            status_code=200)

    def test_status_delete_form(self):
        Status.objects.create(name=self.status)
        response_delete_status = self.client.post('/statuses/1/delete/',
                                                  follow=True)
        self.assertContains(response_delete_status,
                            _('The status has been deleted'),
                            status_code=200)
