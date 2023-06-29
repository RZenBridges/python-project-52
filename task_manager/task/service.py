import django_filters
from .models import Task
from django import forms
from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.label.models import Label


class TaskFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user')
        super(TaskFilter, self).__init__(*args, **kwargs)

    status = django_filters.ModelChoiceFilter(method='status_filter',
                                              queryset=Status.objects.all(),
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control'}))
    performer = django_filters.ModelChoiceFilter(method='performer_filter',
                                                 queryset=User.objects.all(),
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control'}))
    labels = django_filters.ModelChoiceFilter(method='labels_filter',
                                              queryset=Label.objects.all(),
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control'}))
    author = django_filters.BooleanFilter(method='author_filter',
                                          widget=forms.CheckboxInput(
                                              attrs={'class': 'form-check'}),
                                          label='My tasks only')

    def status_filter(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def performer_filter(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def labels_filter(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def author_filter(self, queryset, name, value):
        if value is True:
            return queryset.filter(**{name: self.current_user})
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'performer', 'labels']

