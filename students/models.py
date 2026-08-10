from django.db import models
from django.contrib.auth.models import User
from subjects.models import Topic
from core.models import BaseModel
from django.conf import settings
# Create your models here.

class StudentProgress(BaseModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    highest_unlocked_test = models.IntegerField(default=1)

    class Meta:
        unique_together = ('student', 'topic')
