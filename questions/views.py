from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from accounts.decorators import role_required
from .models import Question
from .forms import QuestionForm
from subjects.models import Subject


@role_required('admin', 'teacher')
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


@role_required('admin', 'teacher', 'student')
def question_list(request):
    user = request.user

    if user.role == 'admin':
        qs = Question.objects.filter(is_active=True)
    elif user.role == 'teacher':
        qs = Question.objects.filter(Q(is_global=True) | Q(created_by=user), is_active=True)
    else:
        qs = Question.objects.filter(is_global=True, status='approved', is_active=True)

    qs = qs.select_related('subject', 'topic', 'created_by')

    search = request.GET.get('search', '').strip()
    subject_id = request.GET.get('subject', '').strip()
    topic_id = request.GET.get('topic', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()

    if search:
        qs = qs.filter(Q(question_text__icontains=search) | Q(explanation__icontains=search))
    if subject_id:
        qs = qs.filter(subject_id=subject_id)
    if topic_id:
        qs = qs.filter(topic_id=topic_id)
    if difficulty:
        qs = qs.filter(difficulty_level=difficulty)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    from subjects.models import Subject
    context = {
        'page_obj': page_obj,
        'subjects': Subject.objects.filter(is_active=True),
        'difficulty_range': range(1, 11),
        'search': search,
        'selected_subject': subject_id,
        'selected_topic': topic_id,
        'selected_difficulty': difficulty,
    }
    return render(request, 'questions/list.html', context)


@role_required('admin', 'teacher')
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


@role_required('admin', 'teacher')
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user.role == 'teacher' and question.created_by_id != request.user.id:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You cannot delete another teacher's question.")

    question.is_active = False
    question.save()
    return redirect('question_list')

@role_required('admin', 'teacher', 'student')
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk, is_active=True)
    user = request.user

    # Enforce the same visibility rule as the list view, at the object level too
    is_visible = (
        user.role == 'admin'
        or (user.role == 'teacher' and (question.is_global or question.created_by_id == user.id))
        or (user.role == 'student' and question.is_global and question.status == 'approved')
    )
    if not is_visible:
        return HttpResponseForbidden("You cannot access this question.")

    # Students never see the correct answer or explanation through the bank
    show_answer = user.role in ('admin', 'teacher')

    return render(request, 'questions/detail.html', {
        'question': question,
        'show_answer': show_answer,
    })