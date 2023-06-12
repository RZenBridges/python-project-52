from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .user.forms import InactiveUserAuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate


NAVIGATION = {
    'title': _('Task manager'),
    'users': _('Users'),
    'log_in': _('Log in'),
    'register': _('Sign up')
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
        username = kwargs.get('username')
        password = kwargs.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('home')
        messages.add_message(request, messages.ERROR, "inserted username or password is faulty")
        return redirect('login')
