from django.contrib import admin

from .models import (
    ConductedExam,
    ConductedExamQuestion,
    ConductedExamParticipant,
    ConductedExamAnswer,
)


# =========================================================
# CONDUCTED EXAM
# =========================================================

@admin.register(ConductedExam)
class ConductedExamAdmin(admin.ModelAdmin):

    list_display = (
        'exam_name',
        'teacher',
        'exam_key',
        'status',
        'duration_minutes',
        'started_at',
        'ends_at',
    )

    list_filter = (
        'status',
        'negative_marking_enabled',
    )

    search_fields = (
        'exam_name',
        'exam_key',
        'teacher__username',
    )

    ordering = (
        '-created_at',
    )


# =========================================================
# CONDUCTED EXAM QUESTION
# =========================================================

@admin.register(ConductedExamQuestion)
class ConductedExamQuestionAdmin(admin.ModelAdmin):

    list_display = (
        'exam',
        'question',
        'question_order',
        'marks',
    )

    list_filter = (
        'exam',
    )

    search_fields = (
        'exam__exam_name',
        'question__question_text',
    )

    ordering = (
        'exam',
        'question_order',
    )


# =========================================================
# CONDUCTED EXAM PARTICIPANT
# =========================================================

@admin.register(ConductedExamParticipant)
class ConductedExamParticipantAdmin(admin.ModelAdmin):

    list_display = (
        'exam',
        'student',
        'status',
        'score',
        'total_marks',
        'violation_count',
        'joined_at',
        'started_at',
        'submitted_at',
    )

    list_filter = (
        'status',
        'exam',
    )

    search_fields = (
        'student__username',
        'student__first_name',
        'student__last_name',
        'exam__exam_name',
        'exam__exam_key',
    )

    ordering = (
        '-joined_at',
    )


# =========================================================
# CONDUCTED EXAM ANSWER
# =========================================================

@admin.register(ConductedExamAnswer)
class ConductedExamAnswerAdmin(admin.ModelAdmin):

    list_display = (
        'participant',
        'exam_question',
        'selected_option',
        'is_correct',
        'marks_obtained',
        'answered_at',
    )

    list_filter = (
        'is_correct',
        'exam_question__exam',
    )

    search_fields = (
        'participant__student__username',
        'participant__exam__exam_name',
    )

    ordering = (
        '-answered_at',
    )