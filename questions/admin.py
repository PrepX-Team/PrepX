from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'subject', 'topic', 'difficulty_level', 'is_global', 'status', 'created_by', 'is_active')
    search_fields = ('question_text', 'explanation')
    list_filter = ('subject', 'difficulty_level', 'is_global', 'status', 'is_active')
    ordering = ('-created_at',)

    def question_text_short(self, obj):
        return obj.question_text[:50]
    question_text_short.short_description = 'Question'