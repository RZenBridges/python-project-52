from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:

        model = Status
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Status Name')
            })
        }
        labels = {
            'name': _('Status Name'),
        }
        error_messages = {
            'name': {
                'unique': _('This name is already taken by another status'),
            },
        }

    def clean_name(self):
        data = self.cleaned_data.get('name')

        try:
            Status.objects.get(name=data)
        except Status.DoesNotExist:
            raise forms.ValidationError('Status has to be unique')
        finally:
            return data
