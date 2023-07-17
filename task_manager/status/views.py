from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .models import Status
from .forms import StatusForm


# ALL STATUSES page
class StatusView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    ordering = ['id']


# CREATE STATUS page
class StatusCreateFormView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    template_name = 'statuses/new_status.html'

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, _('The status has been created'))
        return super().form_valid(form)


# UPDATE STATUS page
class StatusUpdateFormView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm

    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, _('The status has been updated'))
        return HttpResponseRedirect(self.get_success_url())


# DELETE STATUS page
class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status

    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, _('The status has been deleted'))
        return HttpResponseRedirect(self.get_success_url())
