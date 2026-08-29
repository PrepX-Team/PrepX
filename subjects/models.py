from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from core.models import BaseModel


class Subject(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(Lower('name'), name='unique_subject_name_ci'),
        ]
        ordering = ['name']  # for sorting in ascending

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Topic(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            UniqueConstraint(Lower('name'), 'subject', name='unique_topic_name_per_subject_ci'),
        ]
        ordering = ['subject__name', 'name']

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.name} - {self.name}" # QA - Average