from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import LogInForm, UserSignUpForm, UserUpdateForm
from .models import User
from task_manager.mixins import AuthCheckRedirectMixin, NoPermissionMixin,\
    MessageMixin, UserDeleteErrorMixin


# ALL USERS page
class UsersView(ListView):
    model = User
    template_name = 'users/users.html'
    ordering = ['id']


# CREATE USER page
class UsersCreateFormView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'users/new_user.html'
    success_message = _('The user has been registered')


# UPDATE USER page
class UsersUpdateView(SuccessMessageMixin, NoPermissionMixin, AuthCheckRedirectMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    login_url = reverse_lazy('login')
    unauthorized_url = reverse_lazy('users')
    success_url = reverse_lazy('users')
    success_message = _('The user has been updated')


# DELETE USER page
class UsersDeleteView(NoPermissionMixin, AuthCheckRedirectMixin,
                      UserDeleteErrorMixin, DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    unauthorized_url = reverse_lazy('users')
    success_url = reverse_lazy('users')


# LOGIN USER page
class UsersLoginView(MessageMixin, LoginView):
    model = User
    form_class = LogInForm
    redirect_authenticated_user = True
    template_name = 'login.html'
    next_page = reverse_lazy('home')

    success_message = _('You have logged in')
    error_message = _('Enter correct username and password. Both fields can be case-sensitive')


# LOGOUT USER page
class UsersLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _('You have logged out'))
        return super().dispatch(request, *args, **kwargs)
