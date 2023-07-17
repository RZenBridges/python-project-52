from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render

from django.views.generic.base import TemplateView


class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


def error_404(request, exception):
    return render(request, '404.html')