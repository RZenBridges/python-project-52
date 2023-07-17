from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .forms import LabelForm
from .models import Label


# ALL LABELS page
class LabelView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    ordering = ['id']


# CREATE LABEL page
class LabelCreateFormView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm

    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, _('The label has been created'))
        return super().form_valid(form)


# UPDATE LABEL page
class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm

    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, _('The label has been updated'))
        return HttpResponseRedirect(self.get_success_url())


# DELETE STATUS page
class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label

    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, _('The label has been deleted'))
        return HttpResponseRedirect(self.get_success_url())
