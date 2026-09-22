from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'certificate_id', 'completed_at', 'issued_at')
    search_fields = ('student__username', 'topic__name', 'certificate_id')
    readonly_fields = ('student', 'topic', 'certificate_id', 'completed_at', 'issued_at')
