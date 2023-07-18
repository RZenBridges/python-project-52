from django.urls import path
from task_manager.task import views

urlpatterns = [
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_view'),
    path('create/', views.TaskCreateFormView.as_view()),
    path('', views.TaskView.as_view(), name='tasks'),
]
