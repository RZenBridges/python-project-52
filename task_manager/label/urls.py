from django.urls import path
from task_manager.label import views

urlpatterns = [
    path('<int:pk>/update/', views.LabelUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', views.LabelDeleteView.as_view(), name='label_delete'),
    path('create/', views.LabelCreateView.as_view()),
    path('', views.LabelView.as_view(), name='labels'),
]
