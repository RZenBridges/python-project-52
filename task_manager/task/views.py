from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .models import Task
from .forms import TaskForm
# from django.contrib import messages
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
            'column_creator': _('Author'),
            'column_performer': _('Performer'),
            'column_created': _('Created at'),
            'row_edit': _('Edit'),
            'row_delete': _('Delete'),
        }
        tasks = Task.objects.all().order_by('id')
        return render(request,
                      'tasks/tasks.html',
                      context={'tasks_list': tasks} | NAVIGATION | table)


class TaskCreateFormView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'tasks/new_task.html', {'form': form} | NAVIGATION)
