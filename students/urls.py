from django.urls import path
from . import views


urlpatterns = [

    path(
        'exams/join/',
        views.join_exam,
        name='student_join_exam'
    ),

    path(
        'exams/<int:exam_id>/waiting/',
        views.exam_waiting,
        name='student_exam_waiting'
    ),

    path(
        'exams/<int:exam_id>/take/',
        views.take_exam,
        name='student_take_exam',
    ),

    path(
        'exams/<int:exam_id>/submitted/',
        views.exam_submitted,
        name='student_exam_submitted',
    ),

    path(
        'exams/<int:exam_id>/question/<int:exam_question_id>/save/',
        views.save_exam_answer,
        name='student_save_exam_answer',
    ),

    path(
        'exam/<int:exam_id>/waiting-status/',
        views.exam_waiting_status,
        name='student_exam_waiting_status'
    ),

    path(
        'exams/<int:exam_id>/timer-status/',
        views.exam_timer_status,
        name='student_exam_timer_status',
    ),

    path(
        'exams/<int:exam_id>/auto-submit/',
        views.auto_submit_exam,
        name='student_auto_submit_exam',
    ),
]