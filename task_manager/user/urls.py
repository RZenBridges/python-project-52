from django.urls import path

from task_manager.user import views

urlpatterns = [
    path('<int:pk>/update/', views.UsersUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UsersDeleteView.as_view(), name='user_delete'),
    path('create/', views.UsersCreateFormView.as_view()),
    path('', views.UsersView.as_view(), name='users'),
]
