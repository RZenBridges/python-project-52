from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .forms import InactiveUserAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .user.models import User


NAVIGATION = {
    'title': _('Task Manager'),
    'users': _('Users'),
    'statuses': _('Statuses'),
    'tags': _('Tags'),
    'tasks': _('Tasks'),
    'log_in': _('Log in'),
    'log_out': _('Log out'),
    'registration': _('Sign up')
}


class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        index = {
            'greeting': _('Hello, User!'),
            'info': _('Here you can set tasks to the team'),
            'author': _('Learn more about the author')
        }

        return render(request, 'index.html', context=index | NAVIGATION)


class UsersLoginView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = InactiveUserAuthenticationForm()
        return render(request, 'login.html', NAVIGATION | {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.POST.get('username'))
            if user.check_password(request.POST.get('password')):
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('You have logged in'))
                return redirect('home')
        except User.DoesNotExist:
            messages.add_message(
                request,
                messages.ERROR,
                _("Enter correct username and password. Both fields can becase-sensitive"))
        return redirect('login')


class UsersLogoutView(TemplateView):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, _('You have logged out'))
        return redirect('home')
