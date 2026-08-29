from django.contrib import admin

from .models import (
    ExamLog,
    ConductedExamSecurityLog,
)


@admin.register(ExamLog)
class ExamLogAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'event_type', 'timestamp')
    list_filter = ('event_type',)
    search_fields = ('attempt__student__username',)
    ordering = ('-timestamp',)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConductedExamSecurityLog)
class ConductedExamSecurityLogAdmin(admin.ModelAdmin):

    list_display = (
        'participant',
        'event_type',
        'timestamp',
    )

    list_filter = (
        'event_type',
    )

    search_fields = (
        'participant__student__username',
        'participant__exam__exam_name',
        'participant__exam__exam_key',
    )

    ordering = (
        '-timestamp',
    )