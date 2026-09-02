from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from accounts.decorators import role_required

from .models import Result


@role_required('student')
def result_list(request):
    results = (
        Result.objects
        .filter(student=request.user)
        .select_related(
            'practice_attempt__topic__subject',
            'conducted_participant__exam',
        )
        .order_by('-finalized_at')
    )

    page_obj = Paginator(results, 10).get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'results/list.html',
        {
            'page_obj': page_obj,
        },
    )


@role_required('student')
def result_detail(request, result_id):
    result = get_object_or_404(
        Result.objects.select_related(
            'practice_attempt__topic__subject',
            'conducted_participant__exam',
        ),
        pk=result_id,
        student=request.user,
    )

    if result.result_type == 'practice':
        answers = (
            result.practice_attempt.answers
            .select_related('question')
            .order_by('question_order')
        )

        context_answers = [
            {
                'order': answer.question_order,
                'text': answer.question.question_text,
                'selected': answer.selected_option,
                'correct': answer.question.correct_option,
                'explanation': answer.question.explanation,
                'status': (
                    'correct'
                    if answer.is_correct and answer.selected_option
                    else (
                        'unanswered'
                        if answer.selected_option is None
                        else 'incorrect'
                    )
                ),
            }
            for answer in answers
        ]

        attempt = result.practice_attempt

        title = (
            f'{attempt.topic.subject.name} — '
            f'{attempt.topic.name} — '
            f'Test {attempt.test_number}'
        )

        time_taken = (
            attempt.end_time - attempt.start_time
            if attempt.end_time and attempt.start_time
            else None
        )

    else:
        answers = (
            result.conducted_participant.answers
            .select_related('exam_question__question')
            .order_by('exam_question__question_order')
        )

        context_answers = [
            {
                'order': answer.exam_question.question_order,
                'text': answer.exam_question.question.question_text,
                'selected': answer.selected_option,
                'correct': answer.exam_question.question.correct_option,
                'explanation': answer.exam_question.question.explanation,
                'status': (
                    'correct'
                    if answer.is_correct and answer.selected_option
                    else (
                        'unanswered'
                        if answer.selected_option is None
                        else 'incorrect'
                    )
                ),
            }
            for answer in answers
        ]

        participant = result.conducted_participant

        title = participant.exam.exam_name

        time_taken = (
            participant.submitted_at - participant.started_at
            if participant.submitted_at and participant.started_at
            else None
        )

    return render(
        request,
        'results/detail.html',
        {
            'result': result,
            'title': title,
            'answers': context_answers,
            'time_taken': time_taken,
        },
    )