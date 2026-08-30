from django.urls import path
from . import views

urlpatterns = [
    path('exam/<int:attempt_id>/event/', views.log_security_event, name='log_security_event'),

    path(
        'exam/<int:exam_id>/security/event/',
        views.log_exam_security_event,
        name='student_exam_security_event',
    ),
]