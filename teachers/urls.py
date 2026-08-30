from django.urls import path
from . import views

urlpatterns = [
    path(
        'exams/create/',
        views.create_exam,
        name='teacher_create_exam',
    ),

    path(
        'exams/<int:exam_id>/questions/',
        views.select_exam_questions,
        name='teacher_select_exam_questions',
    ),

    path(
        'exams/<int:exam_id>/review/',
        views.review_exam,
        name='teacher_review_exam',
    ),

    path(
        'exams/<int:exam_id>/launch/',
        views.launch_exam,
        name='teacher_launch_exam',
    ),

    path(
        'exams/<int:exam_id>/end/',
        views.end_exam,
        name='teacher_end_exam',
    ),

    path(
        'exams/<int:exam_id>/monitor/',
        views.exam_monitor,
        name='teacher_exam_monitor',
    ),

    path(
        'exams/<int:exam_id>/start/',
        views.start_exam,
        name='teacher_start_exam',
    ),

    path(
        'exams/<int:exam_id>/monitor/data/',
        views.exam_monitor_data,
        name='exam_monitor_data',
    ),

    path(
        'exams/<int:exam_id>/timer-status/',
        views.exam_timer_status,
        name='student_exam_timer_status',
    ),

    path(
        'exams/previous/',
        views.previous_conducted_exams,
        name='teacher_previous_conducted_exams',
    ),

    path(
        'exams/<int:exam_id>/previous-monitor/',
        views.previous_exam_monitor,
        name='teacher_previous_exam_monitor',
    ),

    path(
        'exams/<int:exam_id>/previous-pdf/',
        views.previous_exam_pdf,
        name='teacher_previous_exam_pdf',
    ),

   path(
        'exams/ongoing/',
        views.ongoing_exams,
        name='teacher_ongoing_exams',
    ),
]