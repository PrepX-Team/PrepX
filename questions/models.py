from django.db import models
from django.contrib.auth.models import User
from subjects.models import Subject, Topic
from core.models import BaseModel
from django.conf import settings
# Create your models here.

class Question(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    question_text = models.TextField()

    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()

    correct_option = models.CharField(max_length=1)

    explanation = models.TextField()

    difficulty_level = models.IntegerField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_global = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.question_text[:50]

    class Meta:
        indexes = [
            models.Index(fields=['subject', 'topic']),
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['created_by']),
            models.Index(fields=['is_global', 'status', 'is_active']),
        ]
        ordering = ['-created_at']