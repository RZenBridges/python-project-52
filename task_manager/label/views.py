import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from .forms import LabelForm
from .models import Label


class LabelView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        label_list = Label.objects.all()
        return render(request,
                      'labels/labels.html',
                      context={'label_list': label_list})


class LabelCreateFormView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request,
                      'labels/new_label.html',
                      context={'form': form})

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _('The label has been created'))
            return redirect('labels')
        return render(request,
                      'labels/new_label.html',
                      context={'form': form})


class LabelUpdateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        try:
            label = Label.objects.get(id=label_id)
            form = LabelForm(instance=label)
            return render(request,
                          'labels/update_label.html',
                          {'form': form, 'label_id': label_id})
        except Label.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such label does not exist'))
            logging.warning('Attempted get request to get a non-existing label')
        return redirect('labels')

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        try:
            label = Label.objects.get(id=label_id)
            form = LabelForm(request.POST, instance=label)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, _('The label has been updated'))
                return redirect('labels')
            return render(request, 'labels/update_label.html',
                          {'form': form, 'label_id': label_id})
        except Label.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such label does not exist'))
            logging.warning('Attempted post request to update a non-existing label')

        return redirect('labels')


class LabelDeleteView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        try:
            label = Label.objects.get(id=label_id)
        except Label.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such status does not exist'))
            logging.warning('Attempted get request to get a non-existing label')
            return redirect('statuses')
        return render(request, 'labels/delete_label.html',
                      {'label_id': label_id, 'label_name': label.name})

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        try:
            label = Label.objects.get(id=label_id)
            label.delete()
            messages.add_message(request, messages.SUCCESS,
                                 _('The label has been deleted'))
        except Label.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 _('Such label does not exist'))
            logging.warning('Attempted post request to delete a non-existing label')
        return redirect('labels')
