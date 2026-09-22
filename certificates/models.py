import uuid
from django.conf import settings
from django.db import models
from subjects.models import Topic


class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='certificates')
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    issued_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['student', 'topic'], name='one_certificate_per_student_topic')]
        ordering = ['-issued_at']

    def __str__(self):
        return f'{self.student.username} — {self.topic.name}'
