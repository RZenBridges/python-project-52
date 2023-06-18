from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .models import Task
from .forms import TaskForm
from task_manager.user.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


NAVIGATION = {
    'title': _('Task Manager'),
    'users': _('Users'),
    'statuses': _('Statuses'),
    'tags': _('Tags'),
    'tasks': _('Tasks'),
    'log_in': _('Log in'),
    'log_out': _('Log out'),
    'registration': _('Sign up')
}


# ALL TASKS page
class TaskView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        table = {
            'column_name': _('Task Name'),
            'column_status': _('Status Name'),
            'column_creator': _('Creator'),
            'column_performer': _('Performer'),
            'column_created': _('Created at'),
            'row_edit': _('Edit'),
            'row_delete': _('Delete'),
        }
        tasks = Task.objects.all().order_by('id')
        return render(request,
                      'tasks/tasks.html',
                      context={'task_list': tasks} | NAVIGATION | table)


# CREATE TASK page
class TaskCreateFormView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'tasks/new_task.html', {'form': form} | NAVIGATION)

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['author'] = User.objects.get(id=request.user.id)

        form = TaskForm(data)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        return render(request, 'tasks/new_task.html', {'form': form} | NAVIGATION)


# UPDATE TASK page
class TaskUpdateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        try:
            task = Task.objects.get(id=task_id)
            form = TaskForm(instance=task)
            return render(request,
                          'tasks/update_task.html',
                          NAVIGATION | {'form': form, 'task_id': task_id})

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such task does not exist'))
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
            data['performer'] = User.objects.get(id=data['performer'])

            form = TaskForm(data, instance=task)

            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, _("The task has been updated"))
                return redirect('tasks')
            return render(request, 'tasks/update_task.html',
                          NAVIGATION | {'form': form, 'task_id': task_id})

        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such task does not exist'))
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
            return redirect('tasks')
        return render(request, 'tasks/delete_task.html',
                      NAVIGATION | {'task_id': task_id, 'task_name': task.name})

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
        return redirect('tasks')


class TaskViewView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such task does not exist'))
        return render(request, 'tasks/view_task.html',
                      NAVIGATION | {'task': task})