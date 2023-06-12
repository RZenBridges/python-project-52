from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class InactiveUserAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                'This account is inactive',
                code='inactive')
