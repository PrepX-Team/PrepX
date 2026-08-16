from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('add/', views.add_question, name='add_question'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('<int:pk>/delete/', views.delete_question, name='delete_question'),
]