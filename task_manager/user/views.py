from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import User
from .forms import UserForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


# ALL USERS page
class UsersView(TemplateView):

    def get(self, request, *args, **kwargs):
        table = {
            'column_name': _('User name'),
            'column_fname': _('Full name'),
            'column_created': _('Created at'),
            'row_edit': _('Edit'),
            'row_delete': _('Delete'),
        }
        users = User.objects.all()
        return render(request, 'users.html', context={'user_list': users} | NAVIGATION | table)


# CREATE USER page
class UsersCreateFormView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, 'new_user.html', NAVIGATION | {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid() and form.clean_confirmation():
            form.save()
            messages.add_message(request, messages.INFO, _('The user has been registered'))
            return redirect('login')
#       'Пользователь с таким именем уже существует'
        messages.add_message(request, messages.ERROR, _('Check the inserted data'))
        return render(request, 'new_user.html', NAVIGATION | {'form': form})


# UPDATE USER page
class UsersUpdateView(TemplateView):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if request.user.id == user_id:
            user = User.objects.get(id=user_id)
            form = UserForm(instance=user)
            return render(request, 'update.html', NAVIGATION | {'form': form, 'user_id': user_id})

        elif request.user.is_anonymous:
            messages.add_message(request, messages.ERROR,
                                 _("You are not authenticated! Please, log in."))
            return redirect('login')

        else:
            messages.add_message(request, messages.ERROR,
                                 _("You are not authorized to change other users."))
            return redirect('users')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid and request.user.id == user_id:
            form.save()
            messages.add_message(request, messages.INFO, _("The user has been updated"))
            login(request, user)
            return redirect('users')
        return render(request, 'update.html', {'form': form, 'user_id': user_id})


# DELETE USER page
class UsersDeleteView(TemplateView):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if request.user.id == user_id:
            user = User.objects.get(id=user_id)
            return render(request, 'delete.html', NAVIGATION | {
                'user_id': user_id,
                'fullname': f'{user.first_name} {user.last_name}'
            })

        elif request.user.is_anonymous:
            messages.add_message(request, messages.ERROR,
                                 _("You are not authenticated! Please, log in."))
            return redirect('login')

        messages.add_message(request, messages.ERROR,
                             _("You are not authorized to change other users."))
        return redirect('users')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        if user and request.user.id == user_id:
            user.delete()
            messages.add_message(request, messages.INFO, _("The user has been deleteed"))
        return redirect('users')
