from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
        labels = {
            'name': _('Task Name'),
            'description': _('Task Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels')
        }
