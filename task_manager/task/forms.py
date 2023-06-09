from django import forms
from .models import Task
from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.label.models import Label
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    status = forms.ModelChoiceField(
        label=_('Status'),
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'regDropDown form-control'}),
        empty_label='----',
    )

    executor = forms.ModelChoiceField(
        label=_('Executor'),
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'regDropDown form-control'}),
        empty_label='----'
    )

    labels = forms.ModelMultipleChoiceField(
        label=_('Labels'),
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'regDropDown form-control'}),
        required=False
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'author')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Task Name')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Task Description'),
            })
        }
        labels = {
            'name': _('Task Name'),
            'description': _('Task Description'),
        }
        error_messages = {
            'name': {
                'unique': _('This name is already taken by another task'),
            },
        }
