from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

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
    success_message = _('The task has been created')

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)


# UPDATE TASK page
class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been updated')


# DELETE TASK page
class TaskDeleteView(SuccessMessageMixin, TaskDeletionMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been deleted')


# TASK DETAILS page
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/view_task.html'
    context_object_name = 'task'
