from django.urls import path
from task_manager.task import views

urlpatterns = [
    # path('<int:pk>/update/', views.UsersUpdateView.as_view(), name='user_update'),
    # path('<int:pk>/delete/', views.UsersDeleteView.as_view(), name='user_delete'),
    path('create/', views.TaskCreateFormView.as_view()),
    path('', views.TaskView.as_view(), name='tasks'),
]
