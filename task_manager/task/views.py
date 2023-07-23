from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .forms import TaskForm
from .models import Task
from .filters import TaskFilter
from task_manager.mixins import TaskDeletionMixin


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
class TaskCreateFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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
class TaskDeleteView(TaskDeletionMixin, DeleteView):
    model = Task

    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, _('The task has been deleted'))
        return HttpResponseRedirect(self.get_success_url())


# TASK DETAILS page
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/view_task.html'
    context_object_name = 'task'
