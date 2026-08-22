from django.contrib import admin

from .models import (
    Exam,
    ExamSection,
    ExamAttempt,
    ExamAnswer,
)


admin.site.register(Exam)
admin.site.register(ExamSection)


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "topic",
        "test_number",
        "status",
        "start_time",
        "end_time",
        "score",
        "accuracy",
    )

    search_fields = (
        "student__username",
        "topic__name",
    )

    list_filter = (
        "status",
        "test_number",
        "topic",
    )

    ordering = ("-start_time",)


@admin.register(ExamAnswer)
class ExamAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "question",
        "question_order",
        "selected_option",
        "is_correct",
    )

    search_fields = (
        "attempt__student__username",
    )

    list_filter = (
        "is_correct",
    )