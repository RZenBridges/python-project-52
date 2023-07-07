import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from .forms import InactiveUserAuthenticationForm
from .user.models import User


class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        index = {
            'greeting': _('Hello, User!'),
            'info': _('Here you can set tasks to the team'),
            'author': _('Learn more about the author')
        }

        return render(request, 'index.html', context=index)


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
            messages.add_message(
                request,
                messages.ERROR,
                _('Enter correct username and password. Both fields can becase-sensitive'))
            logging.warning(
                'username or password are incorrect or such user is not registered')

        return redirect('login')


class UsersLogoutView(TemplateView):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, _('You have logged out'))
        return redirect('home')
