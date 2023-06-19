from django import forms
from .models import Task
from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.label.models import Label
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):

    status = forms.ModelChoiceField(
        label='status',
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'regDropDown form-control'}),
        empty_label='----',
        to_field_name='name',
    )

    performer = forms.ModelChoiceField(
        label='performer',
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'regDropDown form-control'}),
        empty_label='----',
        to_field_name='first_name'
    )

    labels = forms.ModelMultipleChoiceField(
        label='labels',
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'regDropDown form-control'}),
        to_field_name='name',
        required=False
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
            'body': forms.Textarea(attrs={
                'label': _('body'),
                'class': 'form-control',
                'placeholder': _('body'),
            })
        }
