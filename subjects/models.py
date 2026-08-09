from django.db import models
from core.models import BaseModel

# Create your models here.

class Subject(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Topic(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('subject', 'name')

    def __str__(self):
        return f"{self.subject.name} - {self.name}"