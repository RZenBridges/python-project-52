from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class UserCheckMixin(LoginRequiredMixin):

    login_url = '/login'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, _('You are not authenticated! Please, log in.'))
            return redirect(self.login_url)
        return redirect(self.success_url)


class CheckUserPermissionMixin(UserPassesTestMixin):

    def test_func(self):
        has_access = self.request.user.is_authenticated and self.request.user == self.get_object()
        if not has_access:
            messages.error(self.request, _('You are not authorized to change other users.'))
        return has_access


class CustomTaskDeletionMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            messages.add_message(self.request, messages.ERROR,
                                 _('You need to be the creator of the task to delete it'))
            return redirect(reverse_lazy('tasks'))

        return super().dispatch(request, *args, **kwargs)


class MessageMixin:

    success_message = ""
    error_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = self.get_error_message(form.cleaned_data)
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_error_message(self, cleaned_data):
        return self.error_message % cleaned_data
