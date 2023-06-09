from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView


NAVIGATION = {
    "title": _("Task manager"),
    "users": _("Users"),
    "log_in": _("Log in"),
    "register": _("Sign up")
}


class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        index = {
            "greeting": _("Hello, User!"),
            "info": _("Here you can set tasks to the team"),
            "author": _("Learn more about the author")
        }

        return render(request, "index.html", context=index | NAVIGATION)


class UsersView(TemplateView):

    def get(self, request, *args, **kwargs):
        table = {
            "column_name": _("User name"),
            "column_fname": _("Full name"),
            "column_created": _("Created at"),
            "row_edit": _("Edit"),
            "row_delete": _("Delete"),
        }
        # Models to be added here
        users = {"items": [{"ID": 1}, {"ID": 2}]}

        return render(request, "users.html", context=users | NAVIGATION | table)


class UsersCreateView(TemplateView):
    pass


class UsersUpdateView(TemplateView):
    pass


class UsersDeleteView(TemplateView):
    pass
