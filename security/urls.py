from django.urls import path
from . import views

urlpatterns = [
    path('exam/<int:attempt_id>/event/', views.log_security_event, name='log_security_event'),
]