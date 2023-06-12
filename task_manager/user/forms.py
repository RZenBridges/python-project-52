from django import forms
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "Two passwords have to match."
    }
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password confirmation'
            }
        )
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'User Name'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }

    def clean_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            return False
        return password_confirmation


class InactiveUserAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                'This account is inactive',
                code='inactive')
