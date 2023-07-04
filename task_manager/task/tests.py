from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.status.models import Status
from task_manager.label.models import Label
from .models import Task


class TaskTest(TestCase):

    def setUp(self):
        self.tasks = Task.objects.all()
        self.username = 'testuser'
        self.password = '12345'
        self.task = 'test_task'
        get_user_model().objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.user = get_user_model().objects.get(username=self.username)
        Status.objects.create(name='test_status')
        Label.objects.create(name='test_label')
        self.status = Status.objects.get(name='test_status')
        self.label = Label.objects.get(name='test_label')

    def test_task_read(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_create_task_db(self):
        task = Task.objects.create(name=self.task, status=self.status,
                                   author=self.user, performer=self.user)
        task.labels.add(self.label)
        self.assertEqual(self.tasks.count(), 1)

    def test_create_task_form(self):
        response_create_task = self.client.post('/tasks/create/',
                                                follow=True,
                                                data={
                                                    'name': self.task,
                                                    'body': self.task,
                                                    'status': 1,
                                                    'author': 1,
                                                    'performer': 1,
                                                })
        self.assertContains(response_create_task,
                            'The task has been created',
                            status_code=200)
        self.assertEqual(self.tasks.count(), 1)

    def test_update_task_form(self):
        Task.objects.create(name=self.task, status=self.status,
                            author=self.user, performer=self.user)
        response_update_task = self.client.post('/tasks/1/update/',
                                                follow=True,
                                                data={
                                                    'name': self.task,
                                                    'body': self.task,
                                                    'status': 1,
                                                    'author': 1,
                                                    'performer': 1,
                                                })
        self.assertContains(response_update_task,
                            'The task has been updated',
                            status_code=200)

    def test_task_delete_form(self):
        Task.objects.create(name=self.task, status=self.status,
                            author=self.user, performer=self.user)
        response_delete_task = self.client.post('/tasks/1/delete/',
                                                follow=True)
        self.assertContains(response_delete_task,
                            'The task has been deleted',
                            status_code=200)
