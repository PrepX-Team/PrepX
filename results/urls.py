from django.urls import path

from . import views


urlpatterns = [
    path('', views.result_list, name='result_list'),
    path('<int:result_id>/', views.result_detail, name='result_detail'),
]