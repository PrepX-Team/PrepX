from django.db import models
from django.contrib.auth.models import User
from subjects.models import Subject, Topic
from core.models import BaseModel
from django.conf import settings

# Create your models here.

class Exam(BaseModel):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.IntegerField()
    exam_key = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title


class ExamSection(BaseModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    difficulty_level = models.IntegerField()
    number_of_questions = models.IntegerField()