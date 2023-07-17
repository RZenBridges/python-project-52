from django import forms
from .models import Task
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Task Name')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Task Description'),
            }),
            'status': forms.Select(attrs={
                'class': 'regDropDown form-control'
            }),
            'executor': forms.Select(attrs={
                'class': 'regDropDown form-control'
            }),
            'labels': forms.SelectMultiple(attrs={
                'class': 'regDropDown form-control'
            }),

        }
        labels = {
            'name': _('Task Name'),
            'description': _('Task Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels')
        }
        error_messages = {
            'name': {
                'unique': _('This name is already taken by another task'),
            },
        }
