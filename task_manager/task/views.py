import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from .forms import TaskForm
from .models import Task
from .service import TaskFilter
from task_manager.label.models import Label
from task_manager.user.models import User


# ALL TASKS page
class TaskView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        f = TaskFilter(request.GET,
                       queryset=Task.objects.all().order_by('id'),
                       current_user=request.user)
        return render(request, 'tasks/tasks.html', context={'filter': f})


# CREATE TASK page
class TaskCreateFormView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'tasks/new_task.html', {'form': form})

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['author'] = User.objects.get(id=request.user.id)
        form = TaskForm(data)
        if form.is_valid():
            task = form.save()
            labels = data.getlist('labels')
            for label in labels:
                task.labels.add(Label.objects.get(id=label))
            messages.add_message(request, messages.SUCCESS, _('The task has been created'))
            return redirect('tasks')

        return render(request, 'tasks/new_task.html', {'form': form})


# UPDATE TASK page
class TaskUpdateView(LoginRequiredMixin, UpdateView):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')

        try:
            task = Task.objects.get(id=task_id)
            form = TaskForm(
                instance=task,
                initial={
                    'status': task.status,
                    'executor': task.executor,
                    'labels': task.labels.all(),
                }
            )
            return render(request, 'tasks/update_task.html', {'form': form, 'task_id': task_id})

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such task does not exist'))
            logging.warning('Attempted get request to get a non-existing task')
            return redirect('tasks')

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')

        try:
            task = Task.objects.get(id=task_id)
            if not task.author_id == request.user.id:
                messages.add_message(request, messages.ERROR,
                                     _('You need to be the creator of the task to delete it'))
                return redirect('tasks')

            data = request.POST.copy()
            data['author'] = User.objects.get(id=request.user.id)
            form = TaskForm(data, instance=task)
            if form.is_valid():
                form.save()
                labels = data.getlist('labels')
                task.labels.set(list(filter(lambda x: str(x.id) in labels, Label.objects.all())))
                task.save()
                messages.add_message(request, messages.SUCCESS, _('The task has been updated'))
                return redirect('tasks')

            return render(request, 'tasks/update_task.html',
                          {'form': form, 'task_id': task_id})

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such task does not exist'))
            logging.warning('Attempted post request to update a non-existing task')

        return redirect('tasks')


# DELETE TASK page
class TaskDeleteView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')

        try:
            task = Task.objects.get(id=task_id)
            if not task.author_id == request.user.id:
                messages.add_message(request, messages.ERROR,
                                     _('You need to be the creator of the task to delete it'))
                return redirect('tasks')

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such task does not exist'))
            logging.warning('Attempted get request to get a non-existing task')
            return redirect('tasks')

        return render(request, 'tasks/delete_task.html',
                      {'task_id': task_id, 'task_name': task.name})

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')

        try:
            task = Task.objects.get(id=task_id)
            if not task.author_id == request.user.id:
                messages.add_message(request, messages.ERROR,
                                     _('You need to be the creator of the task to delete it'))
                return redirect('tasks')
            task.delete()
            messages.add_message(request, messages.SUCCESS,
                                 _('The task has been deleted'))

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such task does not exist'))
            logging.warning('Attempted post request to delete a non-existing task')

        return redirect('tasks')


class TaskViewView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')

        try:
            task = Task.objects.get(id=task_id)
            labels = task.labels.all()

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such task does not exist'))
            logging.warning('Attempted get request to get a non-existing task')

        return render(request,
                      'tasks/view_task.html',
                      {'task': task, 'task_labels': labels, 'author': _('Author'),
                       'executor': _('Executor'), 'task_status': _('Status')})
