from django.shortcuts import render
from django.utils.translation import gettext


def index(request):
    return render(request, 'index.html',
                  context={
                      "greeting": gettext("Hello, User!"),
                      "info": gettext("Here you can set tasks to the team")
                  })
