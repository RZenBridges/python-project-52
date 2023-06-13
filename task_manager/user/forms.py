from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "Two passwords have to match."
    }

    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'label': _('Password Confirmation'),
                'class': 'form-control',
                'placeholder': _('Password (again)')
            }
        )
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'label': _('First Name'),
                'class': 'form-control',
                'placeholder': _('Name')
            }),
            'last_name': forms.TextInput(attrs={
                'label': _('Last Name'),
                'class': 'form-control',
                'placeholder': _('Last Name')
            }),
            'username': forms.TextInput(attrs={
                'label': _('Username'),
                'class': 'form-control',
                'placeholder': _('Username')
            }),
            'password': forms.PasswordInput(attrs={
                'label': _('Password'),
                'class': 'form-control',
                'placeholder': _('Password')
            })
        }

    def clean_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            return False
        return password_confirmation
