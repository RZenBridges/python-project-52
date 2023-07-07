from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django import forms


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

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                'This account is inactive',
                code='inactive')
