from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import DeletionMixin


class MessageMixin(SuccessMessageMixin):
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
        if not request.user.is_authenticated:
            messages.error(self.request, _('You are not authenticated! Please, log in.'))
            return HttpResponseRedirect(self.get_login_url())
        return super().dispatch(request, *args, **kwargs)


class NeedPermitMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user == self.get_object()

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            messages.error(self.request, _('You are not authorized to change other users.'))
            return HttpResponseRedirect(self.unauthorized_url)
        return super().dispatch(request, *args, **kwargs)


class SuccessLogoutMixin:
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, self.success_message)
        return super().dispatch(request, *args, **kwargs)


class UserDeleteErrorMixin(DeletionMixin):
    def post(self, request, *args, **kwargs):
        try:
            response = self.delete(request, *args, **kwargs)
            messages.success(self.request, _('The user has been deleted'))
            return response
        except ProtectedError:
            messages.error(self.request, _('You cannot delete the user that is ascribed a task'))
            return HttpResponseRedirect(self.unauthorized_url)


class StatusDeleteErrorMixin(DeletionMixin):
    def post(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, _('The status has been deleted'))
            return response
        except ProtectedError:
            messages.error(self.request,
                           _('You cannot delete the status that is used in a task'))
            return HttpResponseRedirect(self.get_success_url())


class LabelDeleteErrorMixin(DeletionMixin):
    def post(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, _('The label has been deleted'))
            return response
        except ProtectedError:
            messages.error(self.request,
                           _('You cannot delete the label that is used in a task'))
            return HttpResponseRedirect(self.get_success_url())


class TaskDeletionMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            messages.add_message(self.request, messages.ERROR,
                                 _('You need to be the creator of the task to delete it'))
            return redirect(reverse_lazy('tasks'))

        return super().dispatch(request, *args, **kwargs)
