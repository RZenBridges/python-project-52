import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .forms import TaskForm
from .models import Task
from .service import TaskFilter
from task_manager.custom_mixins import CustomTaskDeletionMixin


# ALL TASKS page
class TaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks.html'

    def get_context_data(self, **kwargs):
        kwargs.update(
            {'filter': TaskFilter(
                self.request.GET,
                queryset=Task.objects.all().order_by('id'),
                current_user=self.request.user)}
        )
        return kwargs


# CREATE TASK page
class TaskCreateFormView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm

    success_url = reverse_lazy('tasks')
    template_name = 'tasks/new_task.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        messages.add_message(self.request, messages.SUCCESS, _('The task has been created'))
        return super().form_valid(form)


# UPDATE TASK page
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm

    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, _('The task has been updated'))
        return HttpResponseRedirect(self.get_success_url())


# DELETE TASK page
class TaskDeleteView(CustomTaskDeletionMixin, DeleteView):
    model = Task

    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, _('The task has been deleted'))
        return HttpResponseRedirect(self.get_success_url())


# TASK DETAILS page
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
                       'executor': _('Executor'), 'status': _('Status')})
