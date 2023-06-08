from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    return render(request, 'index.html',
                  context={
                      "greeting": _("Hello, User!"),
                      "info": _("Here you can set tasks to the team"),
                      "author": _("Learn more about the author"),
                      "title": _("Task manager"),
                      "users": _("Users"),
                      "log": _("Log in"),
                      "register": _("Sign up")
                  })
