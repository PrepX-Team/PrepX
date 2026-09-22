from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('<uuid:certificate_id>/download/', views.certificate_pdf, name='certificate_pdf'),
    path('verify/<uuid:certificate_id>/', views.certificate_verify, name='certificate_verify'),
]
