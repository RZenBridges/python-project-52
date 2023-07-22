from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import LogInForm, UserSignUpForm
from .models import User
from task_manager.mixins import UserCheckMixin, CheckUserPermissionMixin, MessageMixin


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
class UsersUpdateView(UserCheckMixin, CheckUserPermissionMixin, UpdateView):
    model = User
    form_class = UserSignUpForm

    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users')
    success_message = _('The user has been updated')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        login(self.request, user=User.objects.get(username=self.object.username))
        return self.success_url


# DELETE USER page
class UsersDeleteView(MessageMixin, UserCheckMixin, CheckUserPermissionMixin, DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users')

    success_message = _('The user has been deleted')
    error_message = _('You cannot delete the user that is ascribed a task')

    def form_valid(self, form):
        try:
            self.delete(self.request)
            messages.success(self.request, _('The user has been deleted'))
        except ProtectedError:
            messages.error(self.request, _('You cannot delete the user that is ascribed a task'))
        return HttpResponseRedirect(self.get_success_url())


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
