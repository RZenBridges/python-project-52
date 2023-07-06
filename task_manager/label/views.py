from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LabelForm
from .models import Label

NAVIGATION = {
    'title': _('Task Manager'),
    'users': _('Users'),
    'statuses': _('Statuses'),
    'labels': _('Labels'),
    'tasks': _('Tasks'),
    'log_in': _('Sign in'),
    'log_out': _('Log out'),
    'registration': _('Sign up'),
}


class LabelView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        table = {
            'column_name': _('Status name'),
            'column_created': _('Created at'),
            'row_edit': _('Edit'),
            'row_delete': _('Delete'),
        }
        label_list = Label.objects.all()
        return render(request,
                      'labels/labels.html',
                      context={'label_list': label_list} | NAVIGATION | table)


class LabelCreateFormView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request,
                      'labels/new_label.html',
                      context={'form': form} | NAVIGATION)

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("The label has been created"))
            return redirect('labels')
        return render(request,
                      'labels/new_label.html',
                      context={'form': form} | NAVIGATION)


class LabelUpdateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        try:
            label = Label.objects.get(id=label_id)
            form = LabelForm(instance=label)
            return render(request,
                          'labels/update_label.html',
                          NAVIGATION | {'form': form, 'label_id': label_id})
        except Label.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such label does not exist'))
        return redirect('labels')

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = Label.objects.get(id=label_id)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("The label has been updated"))
            return redirect('labels')
        return render(request, 'labels/update_label.html',
                      NAVIGATION | {'form': form, 'label_id': label_id})


class LabelDeleteView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        try:
            label = Label.objects.get(id=label_id)
        except Label.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Such status does not exist'))
            return redirect('statuses')
        return render(request, 'labels/delete_label.html',
                      NAVIGATION | {'label_id': label_id, 'label_name': label.name})

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
        # If a label is linked to a task, then the label cannot be deleted
        return redirect('labels')
