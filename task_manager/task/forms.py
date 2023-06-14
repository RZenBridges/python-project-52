from django import forms
from .models import Task
from task_manager.status.models import Status
from task_manager.user.models import User
from django.utils.translation import gettext_lazy as _

CHOICES = [('1', 'First'), ('2', 'Second')]

status_list = Status.objects.all()
user_list = User.objects.all()


class TaskForm(forms.ModelForm):

    status = forms.ChoiceField(
        label='status',
        choices=[('0', '----')] + [(status.id, status.name) for status in status_list],
        widget=forms.Select(attrs={'class': 'regDropDown form-control'}),
        initial=0
    )

    performer = forms.ChoiceField(
        label='performer',
        choices=[('0', '----')] + [(user.id, user.username) for user in user_list],
        widget=forms.Select(attrs={'class': 'regDropDown form-control'}),
        initial=0
    )

    class Meta:
        model = Task
        fields = ('name', 'body', 'status', 'performer')
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
