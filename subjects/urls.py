from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('add/', views.add_subject, name='add_subject'),
    path('topic/add/', views.add_topic, name='add_topic'),
    path('<int:pk>/delete/', views.delete_subject, name='delete_subject'),
]