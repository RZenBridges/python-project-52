from django.urls import path
from task_manager.status import views

urlpatterns = [
    path('<int:pk>/update/', views.StatusUpdateFormView.as_view(), name='status_update'),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
    path('create/', views.StatusCreateView.as_view()),
    path('', views.StatusView.as_view(), name='statuses'),
]
