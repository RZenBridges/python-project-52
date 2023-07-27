import django_filters
from .models import Task
from django import forms
from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.label.models import Label
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'author']

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label_suffix='',
        label=_('Status')
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label_suffix='',
        label=_('Executor'),
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label_suffix='',
        label=_('Label'),
    )
    author = django_filters.BooleanFilter(
        method='author_filter',
        widget=forms.CheckboxInput(),
        label_suffix='',
        label=_('My tasks only'),
    )

    def author_filter(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
