import re
from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):

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

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 3:
            raise forms.ValidationError('The password is too short')
        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError('Has to match the password')
        return password_confirmation

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.fullmatch(r'^[\w@\+\-\.]+', username):
            raise forms.ValidationError('Has forbidden characters')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('This username is already taken')
        finally:
            return username
