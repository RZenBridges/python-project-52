import re
from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

FIRST_NAME = _('First Name')
LAST_NAME = _('Last Name')
USERNAME = _('Username')
PASSWORD = _('Password')


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    password1 = forms.CharField(
        label=PASSWORD,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': PASSWORD,
            }
        )
    )

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
        fields = ('first_name', 'last_name', 'username')
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
            })
        }
        labels = {
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
            'username': USERNAME,
            'password': PASSWORD,
        }

        error_messages = {
            'username': {
                'unique': _('This name is already taken by another user'),
            },
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Has to match the password')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #
    #     if not re.fullmatch(r'^[\w@\+\-\.]+', username):
    #         raise forms.ValidationError('Has forbidden characters')
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('This username is already taken')
    #     return username


class InactiveUserAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Username'),
            }
        ),
        label=_('Username'),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
            }
        ),
        label=_('Password')
    )

    class Meta:
        fields = ('username', 'password1')

    # def confirm_login_allowed(self, user):
    #     if not user.is_active:
    #         raise ValidationError('This account is inactive', code='inactive')