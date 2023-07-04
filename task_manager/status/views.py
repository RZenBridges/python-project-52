from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .models import Status
from .forms import StatusForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


NAVIGATION = {
    'title': _('Task Manager'),
    'users': _('Users'),
    'statuses': _('Statuses'),
    'labels': _('Labels'),
    'tasks': _('Tasks'),
    'log_in': _('Log in'),
    'log_out': _('Log out'),
    'registration': _('Sign up')
}


# ALL STATUSES page
class StatusView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        table = {
            'column_name': _('Status Name'),
            'column_created': _('Created at'),
            'row_edit': _('Edit'),
            'row_delete': _('Delete'),
        }
        statuses = Status.objects.all().order_by('id')
        return render(request,
                      'statuses/statuses.html',
                      context={'status_list': statuses} | NAVIGATION | table)


class StatusCreateFormView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'statuses/new_status.html', {'form': form} | NAVIGATION)

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("The status has been created"))
            return redirect('statuses')
        return render(request, 'statuses/new_status.html', {'form': form} | NAVIGATION)


class StatusUpdateFormView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        try:
            status = Status.objects.get(id=status_id)
            form = StatusForm(instance=status)
            return render(request,
                          'statuses/update_status.html',
                          NAVIGATION | {'form': form, 'status_id': status_id})
        except Status.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such status does not exist'))
        return redirect('statuses')

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = Status.objects.get(id=status_id)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("The status has been updated"))
            return redirect('statuses')
        return render(request, 'statuses/update_status.html',
                      NAVIGATION | {'form': form, 'status_id': status_id})


class StatusDeleteView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        try:
            status = Status.objects.get(id=status_id)
        except Status.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such status does not exist'))
            return redirect('statuses')
        return render(request, 'statuses/delete_status.html',
                      NAVIGATION | {'status_id': status_id, 'status_name': status.name})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        try:
            status = Status.objects.get(id=status_id)
            status.delete()
            messages.add_message(request, messages.SUCCESS,
                                 _('The status has been deleted'))
        except Status.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such status does not exist'))
        # If a task linked to the status exist then the status cannot be deleted
        return redirect('statuses')
