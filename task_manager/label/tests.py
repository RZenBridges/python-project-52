from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Label
from django.utils.translation import gettext as _


class LabelTest(TestCase):

    def setUp(self):
        self.labels = Label.objects.all()
        self.username = 'testuser'
        self.password = '12345'
        self.label = 'test_label'
        self.label_upd = 'test_label_upd'
        get_user_model().objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_create_label_db(self):
        Label.objects.create(name=self.label)
        self.assertEqual(self.labels.count(), 1)
        self.assertEqual(self.labels.first().name, self.label)

    def test_create_label_form(self):
        response_create_label = self.client.post('/labels/create/',
                                                 follow=True,
                                                 data={'name': self.label})
        self.assertContains(response_create_label,
                            _('The label has been created'),
                            status_code=200)
        self.assertEqual(self.labels.count(), 1)
        self.assertEqual(self.labels.first().name, self.label)

    def test_update_label_form(self):
        Label.objects.create(name=self.label)
        response_update_label = self.client.post('/labels/1/update/',
                                                 follow=True,
                                                 data={'name': self.label_upd})
        self.assertContains(response_update_label,
                            _('The label has been updated'),
                            status_code=200)
        self.assertEqual(self.labels.first().name, self.label_upd)

    def test_label_delete_form(self):
        Label.objects.create(name=self.label)
        response_delete_label = self.client.post('/labels/1/delete/',
                                                 follow=True)
        self.assertContains(response_delete_label,
                            _('The label has been deleted'),
                            status_code=200)
        self.assertEqual(self.labels.count(), 0)
