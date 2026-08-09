from django.db import models
from django.contrib.auth.models import User
from exams.models import Exam
from core.models import BaseModel
# Create your models here.

class Result(BaseModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"