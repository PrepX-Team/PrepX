from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'result_type',
        'score',
        'total_marks',
        'accuracy',
        'finalized_at',
    )

    search_fields = (
        'student__username',
        'student__email',
    )

    list_filter = (
        'finalized_at',
    )

    ordering = (
        '-finalized_at',
    )

    readonly_fields = (
        'student',
        'practice_attempt',
        'conducted_participant',
        'finalized_at',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False