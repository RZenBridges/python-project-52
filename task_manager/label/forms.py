from django import forms
from .models import Label
from django.utils.translation import gettext_lazy as _


class LabelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Label
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Label Name'),
            })
        }
        labels = {
            'name': _('Label Name'),
        }
        error_messages = {
            'name': {
                'unique': _('This name is already taken by another label'),
            },
        }
