from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserUpdateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.username == username:
            return username
        return super().clean_username()


class LogInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
