from django import forms
from .models import Subject, Topic


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'name']