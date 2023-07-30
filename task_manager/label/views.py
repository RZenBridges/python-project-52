from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .forms import LabelForm
from .models import Label
from task_manager.mixins import DeleteErrorMixin


# ALL LABELS page
class LabelView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    ordering = ['id']


# CREATE LABEL page
class LabelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels')
    success_message = _('The label has been created')


# UPDATE LABEL page
class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('labels')
    success_message = _('The label has been updated')


# DELETE STATUS page
class LabelDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteErrorMixin, DeleteView):
    model = Label
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('labels')
    success_message = _('The label has been deleted')
    reject_message = _('You cannot delete the label that is used in a task')
