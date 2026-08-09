from django.db import models
from django.contrib.auth.models import User
from subjects.models import Topic
from core.models import BaseModel
# Create your models here.

class StudentProgress(BaseModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    highest_unlocked_test = models.IntegerField(default=1)

    class Meta:
        unique_together = ('student', 'topic')