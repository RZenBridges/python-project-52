from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class LogInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
