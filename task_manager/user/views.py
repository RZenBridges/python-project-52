from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from .forms import InactiveUserAuthenticationForm, UserForm
from .models import User
from task_manager.custom_mixins import CustomLoginRequiredMixin


# ALL USERS page
class UsersView(ListView):
    model = User
    template_name = 'users/users.html'
    ordering = ['id']


# CREATE USER page
class UsersCreateFormView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    template_name = 'users/new_user.html'

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, _('The user has been registered'))
        return super().form_valid(form)


# UPDATE USER page
class UsersUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm

    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, user=User.objects.get(username=self.object.username))
        messages.add_message(self.request, messages.SUCCESS, _('The user has been updated'))
        return HttpResponseRedirect(self.get_success_url())


# DELETE USER page
class UsersDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = User

    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        if self.object.executor.count() > 0:
            messages.add_message(self.request,
                                 messages.ERROR,
                                 _('You cannot delete the user that is ascribed a task'))
            return HttpResponseRedirect(self.get_success_url())
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, _('The user has been deleted'))
        return HttpResponseRedirect(self.get_success_url())


class UsersLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = InactiveUserAuthenticationForm()
        if request.user.is_anonymous:
            return render(request, 'login.html', {'form': form})

        return redirect('home')

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.POST.get('username'))
            if user.check_password(request.POST.get('password1')):
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('You have logged in'))
                return redirect('home')

        except User.DoesNotExist:
            pass

        messages.add_message(
            request,
            messages.ERROR,
            _('Enter correct username and password. Both fields can be case-sensitive')
        )
        return redirect('login')


# LOGOUT USER page
class UsersLogoutView(TemplateView):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, _('You have logged out'))
        return redirect('home')
