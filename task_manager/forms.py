from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django import forms


class InactiveUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'label': _('Username'),
                'class': 'form-control',
                'placeholder': _('Username'),
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'label': _('Password'),
                'class': 'form-control',
                'placeholder': _('Password'),
            }
        )
    )

    class Meta:
        fields = ('username', 'password')

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                'This account is inactive',
                code='inactive')
