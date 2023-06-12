from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import User
from .forms import UserForm
from django.contrib import messages
from django.utils.translation import gettext as _


NAVIGATION = {
    'title': _('Task manager'),
    'users': _('Users'),
    'log_in': _('Log in'),
    'register': _('Sign up')
}


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


class UsersCreateFormView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, 'new_user.html', NAVIGATION | {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid() and form.clean_confirmation():
            form.save()
            messages.add_message(request, messages.INFO, 'Пользователь успешно зарегистрирован')
            return redirect('users')
#       'Пользователь с таким именем уже существует'
        messages.add_message(request, messages.ERROR, 'Проверьте данные')
        return render(request, 'new_user.html', NAVIGATION | {'form': form})


class UsersUpdateView(TemplateView):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(request, 'update.html', NAVIGATION | {'form': form, 'user_id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            messages.add_message(request, messages.INFO, "Пользователь успешно изменен")
            return redirect('users')
        return render(request, 'update.html', {'form': form, 'user_id': user_id})


class UsersDeleteView(TemplateView):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        return render(request, 'delete.html', NAVIGATION | {
            'user_id': user_id,
            'fullname': f'{user.first_name} {user.last_name}'
        })

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
            messages.add_message(request, messages.INFO, "Пользователь успешно удален")
        return redirect('users')
