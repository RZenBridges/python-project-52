from django import forms
from .models import Task
from task_manager.status.models import Status
from task_manager.user.models import User
from django.utils.translation import gettext_lazy as _

CHOICES = [('1', 'First'), ('2', 'Second')]


class TaskForm(forms.ModelForm):

    status = forms.ModelChoiceField(
        label='status',
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'regDropDown form-control'}),
        empty_label='----'
    )

    performer = forms.ModelChoiceField(
        label='performer',
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'regDropDown form-control'}),
        empty_label='----'
    )

    class Meta:
        model = Task
        fields = ('name', 'body', 'status', 'performer', 'author')
        widgets = {
            'name': forms.TextInput(attrs={
                'label': _('name'),
                'class': 'form-control',
                'placeholder': _('name')
            }),
            'body': forms.TextInput(attrs={
                'label': _('body'),
                'class': 'form-control',
                'placeholder': _('body')
            })
        }
