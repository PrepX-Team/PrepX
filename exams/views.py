from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
import json

from django.http import (
    JsonResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.utils import timezone

from .services.timer import get_remaining_seconds, is_editable
from .models import ExamAttempt, ExamAnswer

from accounts.decorators import role_required
from subjects.models import Subject, Topic

from .services.practice import (
    start_practice_attempt,
    get_unlocked_test_number,
    get_eligible_questions,
    PracticeError,
)
from core.constants import (
    MIN_TEST_NUMBER,
    MAX_TEST_NUMBER,
    QUESTIONS_PER_TEST,
)

def _get_owned_attempt_or_none(request, attempt_id):
    return ExamAttempt.objects.filter(
        pk=attempt_id,
        student=request.user,
    ).first()

@role_required('student')
@require_POST
def practice_answer_save(request, attempt_id):
    attempt = _get_owned_attempt_or_none(request, attempt_id)

    if attempt is None:
        return JsonResponse(
            {
                'success': False,
                'error': 'Attempt not found.',
            },
            status=403,
        )

    if not is_editable(attempt):
        return JsonResponse(
            {
                'success': False,
                'error': 'This attempt is no longer editable.',
            },
            status=409,
        )

    try:
        payload = json.loads(request.body)

        question_id = int(payload.get('question_id'))
        selected_option = payload.get('selected_option')
        marked_for_review = payload.get('marked_for_review', False)
        time_spent = int(payload.get('time_spent', 0))

    except (TypeError, ValueError, json.JSONDecodeError):
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid request.',
            },
            status=400,
        )

    # Validate selected option.
    if selected_option not in (None, 'A', 'B', 'C', 'D'):
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid option.',
            },
            status=400,
        )

    # Validate marked_for_review.
    if not isinstance(marked_for_review, bool):
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid review flag.',
            },
            status=400,
        )

    # Never trust question_id.
    # It must belong to THIS attempt.
    answer = ExamAnswer.objects.filter(
        attempt=attempt,
        question_id=question_id,
    ).first()

    if answer is None:
        return JsonResponse(
            {
                'success': False,
                'error': 'This question is not part of this attempt.',
            },
            status=400,
        )

    # time_spent is an incremental number of seconds reported
    # since the previous save for this answer.
    if not 0 <= time_spent <= 3600:
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid time value.',
            },
            status=400,
        )

    if selected_option is not None:
        answer.selected_option = selected_option

    answer.marked_for_review = marked_for_review
    answer.time_spent += time_spent

    answer.save(
        update_fields=[
            'selected_option',
            'marked_for_review',
            'time_spent',
        ]
    )

    return JsonResponse({
        'success': True,
    })

@role_required('student')
def practice_timer_status(request, attempt_id):
    attempt = _get_owned_attempt_or_none(request, attempt_id)

    if attempt is None:
        return JsonResponse(
            {
                'success': False,
                'error': 'Attempt not found.',
            },
            status=403,
        )

    return JsonResponse({
        'remaining_seconds': get_remaining_seconds(attempt),
        'server_time': timezone.now().isoformat(),
        'attempt_status': attempt.status,
        'editable': is_editable(attempt),
    })

@role_required("student")
def practice_home(request):
    subjects = Subject.objects.filter(is_active=True)

    return render(
        request,
        "exams/practice_home.html",
        {"subjects": subjects},
    )


@role_required("student")
def practice_topics(request, subject_id):
    subject = get_object_or_404(
        Subject,
        pk=subject_id,
        is_active=True,
    )

    topics = subject.topics.filter(is_active=True)

    return render(
        request,
        "exams/practice_topics.html",
        {
            "subject": subject,
            "topics": topics,
        },
    )


@role_required("student")
def practice_tests(request, topic_id):
    topic = get_object_or_404(
        Topic,
        pk=topic_id,
        is_active=True,
        subject__is_active=True,
    )

    unlocked = get_unlocked_test_number(
        request.user,
        topic,
    )

    tests = []

    for number in range(
        MIN_TEST_NUMBER,
        MAX_TEST_NUMBER + 1,
    ):
        available_count = get_eligible_questions(
            topic,
            number,
        ).count()

        tests.append(
            {
                "number": number,
                "unlocked": number <= unlocked,
                "available": available_count >= QUESTIONS_PER_TEST,
                "available_count": available_count,
            }
        )

    return render(
        request,
        "exams/practice_tests.html",
        {
            "topic": topic,
            "tests": tests,
        },
    )


@role_required("student")
def practice_instructions(request, topic_id, test_number):
    topic = get_object_or_404(
        Topic,
        pk=topic_id,
        is_active=True,
        subject__is_active=True,
    )

    test_number = int(test_number)

    unlocked = get_unlocked_test_number(
        request.user,
        topic,
    )

    if (
        not (
            MIN_TEST_NUMBER
            <= test_number
            <= MAX_TEST_NUMBER
        )
        or test_number > unlocked
    ):
        messages.error(
            request,
            "This test is currently locked.",
        )

        return redirect(
            "practice_tests",
            topic_id=topic.id,
        )

    return render(
        request,
        "exams/practice_instructions.html",
        {
            "topic": topic,
            "test_number": test_number,
            "questions_per_test": QUESTIONS_PER_TEST,
        },
    )


@role_required("student")
@require_POST
def practice_start(request, topic_id, test_number):
    topic = get_object_or_404(
        Topic,
        pk=topic_id,
        is_active=True,
        subject__is_active=True,
    )

    test_number = int(test_number)

    try:
        attempt = start_practice_attempt(
            request.user,
            topic,
            test_number,
        )

    except PracticeError as error:
        messages.error(
            request,
            str(error),
        )

        return redirect(
            "practice_tests",
            topic_id=topic.id,
        )

    return redirect(
        "practice_attempt",
        attempt_id=attempt.id,
    )


@role_required('student')
def practice_attempt(request, attempt_id):
    attempt = get_object_or_404(
        ExamAttempt,
        pk=attempt_id,
    )

    if attempt.student_id != request.user.id:
        return HttpResponseForbidden(
            "You cannot access another student's attempt."
        )

    answers = (
        attempt.answers
        .select_related('question')
        .order_by('question_order')
    )

    # JSON-safe data for the frontend.
    # NEVER include correct_option or explanation.
    questions_data = [
        {
            'question_id': answer.question_id,
            'order': answer.question_order,
            'text': answer.question.question_text,
            'options': {
                'A': answer.question.option_a,
                'B': answer.question.option_b,
                'C': answer.question.option_c,
                'D': answer.question.option_d,
            },
            'selected_option': answer.selected_option,
            'marked_for_review': answer.marked_for_review,
        }
        for answer in answers
    ]

    return render(
        request,
        'exams/practice_attempt.html',
        {
            'attempt': attempt,
            'answers': answers,
            'questions_json': json.dumps(questions_data),
            'remaining_seconds': get_remaining_seconds(attempt),
            'editable': is_editable(attempt),
        },
    )