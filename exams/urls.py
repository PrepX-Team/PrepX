from django.urls import path

from . import views


urlpatterns = [
    path("practice/",views.practice_home,name="practice_home",),
    path("practice/<int:subject_id>/",views.practice_topics,name="practice_topics",),
    path("practice/topic/<int:topic_id>/",views.practice_tests,name="practice_tests",),
    path("practice/topic/<int:topic_id>/test/<int:test_number>/",views.practice_instructions,name="practice_instructions",),
    path("practice/topic/<int:topic_id>/test/<int:test_number>/start/",views.practice_start,name="practice_start",),
    path("practice/attempt/<int:attempt_id>/",views.practice_attempt,name="practice_attempt",),
    path('practice/attempt/<int:attempt_id>/answer/', views.practice_answer_save, name='practice_answer_save'),
    path('practice/attempt/<int:attempt_id>/timer/', views.practice_timer_status, name='practice_timer_status'),
]