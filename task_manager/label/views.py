from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

NAVIGATION = {
    'title': _('Task Manager'),
    'users': _('Users'),
    'statuses': _('Statuses'),
    'labels': _('Labels'),
    'tags': _('Tags'),
    'tasks': _('Tasks'),
    'log_in': _('Log in'),
    'log_out': _('Log out'),
    'registration': _('Sign up')
}


class LabelView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        table = {
            'column_name': _('Status Name'),
            'column_created': _('Created at'),
            'row_edit': _('Edit'),
            'row_delete': _('Delete'),
        }
        label_list = []
        return render(request,
                      'labels/labels.html',
                      context={'label_list': label_list} | NAVIGATION | table)


class LabelCreateFormView(LoginRequiredMixin, TemplateView):

    def get(self, requst, *args, **kwargs):
        pass

    def post(self, requst, *args, **kwargs):
        pass


class LabelUpdateView(LoginRequiredMixin, TemplateView):

    def get(self, requst, *args, **kwargs):
        pass

    def post(self, requst, *args, **kwargs):
        pass


class LabelDeleteView(LoginRequiredMixin, TemplateView):

    def get(self, requst, *args, **kwargs):
        pass

    def post(self, requst, *args, **kwargs):
        pass
