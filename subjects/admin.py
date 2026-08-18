from django.contrib import admin
from .models import Subject, Topic

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)
    ordering = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'is_active', 'created_at')
    search_fields = ('name', 'subject__name')
    list_filter = ('subject', 'is_active')
    ordering = ('subject__name', 'name')