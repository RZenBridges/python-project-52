from django import forms
from .models import Status
from django.utils.translation import gettext_lazy as _


class StatusForm(forms.ModelForm):

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
            'name': _('Status Name')
        }

    def clean_name(self):
        data = self.cleaned_data.get('name')

        try:
            Status.objects.get(name=data)
        except Status.DoesNotExist:
            raise forms.ValidationError('Status has to be unique')
        finally:
            return data
