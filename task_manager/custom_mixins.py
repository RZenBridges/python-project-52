from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class CustomLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR,
                                 _('You are not authenticated! Please, log in.'))
            return redirect('/login')

        elif request.user.is_authenticated and self.request.user != self.get_object():
            messages.add_message(self.request, messages.ERROR,
                                 _('You are not authorized to change other users.'))
            return redirect(reverse_lazy('users'))

        return super().dispatch(request, *args, **kwargs)


class CustomTaskDeletionMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            messages.add_message(self.request, messages.ERROR,
                                 _('You need to be the creator of the task to delete it'))
            return redirect(reverse_lazy('tasks'))

        return super().dispatch(request, *args, **kwargs)