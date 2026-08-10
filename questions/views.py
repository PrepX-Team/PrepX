from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from accounts.decorators import role_required
from .models import Question
from .forms import QuestionForm


@role_required(['admin', 'teacher'])
def add_question(request):
    form = QuestionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        question = form.save(commit=False)
        question.created_by = request.user
        question.is_global = (request.user.role == 'admin')
        question.status = 'approved' if request.user.role == 'admin' else 'pending'
        question.save()
        return redirect('question_list')

    return render(request, 'questions/add_question.html', {'form': form})


@role_required(['admin', 'teacher', 'student'])
def question_list(request):
    user = request.user

    if user.role == 'admin':
        qs = Question.objects.filter(is_active=True)
    elif user.role == 'teacher':
        qs = Question.objects.filter(
            Q(is_global=True) | Q(created_by=user),
            is_active=True
        )
    else:  # student
        qs = Question.objects.filter(is_global=True, status='approved', is_active=True)

    # Filters
    subject_id = request.GET.get('subject')
    topic_id = request.GET.get('topic')
    difficulty = request.GET.get('difficulty')

    if subject_id:
        qs = qs.filter(subject_id=subject_id)
    if topic_id:
        qs = qs.filter(topic_id=topic_id)
    if difficulty:
        qs = qs.filter(difficulty_level=difficulty)

    return render(request, 'questions/list.html', {
        'questions': qs.select_related('subject', 'topic')
    })


@role_required(['admin', 'teacher'])
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user.role == 'teacher' and question.created_by_id != request.user.id:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You cannot edit another teacher's question.")

    form = QuestionForm(request.POST or None, instance=question)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('question_list')

    return render(request, 'questions/add_question.html', {'form': form, 'editing': True})


@role_required(['admin', 'teacher'])
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user.role == 'teacher' and question.created_by_id != request.user.id:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You cannot delete another teacher's question.")

    question.is_active = False
    question.save()
    return redirect('question_list')