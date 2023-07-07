import re
from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _


FIRST_NAME = _('First Name')
LAST_NAME = _('Last Name')
USERNAME = _('Username')
PASSWORD = _('Password')


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password (again)')
            }),
        label=_('Password Confirmation')
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': FIRST_NAME,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': LAST_NAME,
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': USERNAME,
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': PASSWORD
            })
        }
        labels = {
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
            'username': USERNAME,
            'password': PASSWORD
        }
        error_messages = {
            'username': {
                'unique': _('This name is already taken by another user'),
            },
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 3:
            raise forms.ValidationError('The password is too short')
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Has to match the password')
        return password2

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
