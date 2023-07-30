from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class FeedbackMixin(SuccessMessageMixin):
    error_message = ""

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = self.get_error_message(form.cleaned_data)
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_error_message(self, cleaned_data):
        return self.error_message % cleaned_data


class NeedAuthMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('You are not authenticated! Please, log in.')
        self.redirect_url = reverse_lazy('login')
        return super().dispatch(request, *args, **kwargs)


class HandleNoPermissionMixin:
    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.redirect_url)


class NeedPermitMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object()

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('You are not authorized to change other users.')
        self.redirect_url = reverse_lazy('users')
        return super().dispatch(request, *args, **kwargs)


class DeleteErrorMixin:
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, self.reject_message)
            return HttpResponseRedirect(self.success_url)
