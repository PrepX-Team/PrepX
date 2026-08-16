from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Subject, Topic
from .forms import SubjectForm, TopicForm


@login_required
def subject_list(request):
    subjects = Subject.objects.filter(is_active=True).prefetch_related('topic_set')
    return render(request, 'subjects/list.html', {'subjects': subjects})


@role_required('admin')
def add_subject(request):
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'subjects/add_subject.html', {'form': form})


@role_required('admin')
def add_topic(request):
    form = TopicForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'subjects/add_topic.html', {'form': form})


@role_required('admin')
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.is_active = False   # soft delete
    subject.save()
    return redirect('subject_list')