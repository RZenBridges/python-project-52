import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from .models import Status
from .forms import StatusForm


# ALL STATUSES page
class StatusView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all().order_by('id')
        return render(request,
                      'statuses/statuses.html',
                      context={'status_list': statuses})


class StatusCreateFormView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'statuses/new_status.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _('The status has been created'))
            return redirect('statuses')
        return render(request, 'statuses/new_status.html', {'form': form})


class StatusUpdateFormView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        try:
            status = Status.objects.get(id=status_id)
            form = StatusForm(instance=status)
            return render(request,
                          'statuses/update_status.html',
                          {'form': form, 'status_id': status_id})

        except Status.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such status does not exist'))
            logging.warning('Attempted get request to get a non-existing status')
        return redirect('statuses')

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        try:
            status = Status.objects.get(id=status_id)
            form = StatusForm(request.POST, instance=status)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, _('The status has been updated'))
                return redirect('statuses')
            return render(request,
                          'statuses/update_status.html',
                          {'form': form, 'status_id': status_id})

        except Status.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such status does not exist'))
            logging.warning('Attempted post request to update a non-existing status')

        return redirect('statuses')


class StatusDeleteView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        try:
            status = Status.objects.get(id=status_id)
        except Status.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such status does not exist'))
            logging.warning('Attempted get request to get a non-existing status')
            return redirect('statuses')
        return render(request, 'statuses/delete_status.html',
                      {'status_id': status_id, 'status_name': status.name})

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
            logging.warning('Attempted post request to delete a non-existing status')
        return redirect('statuses')
