from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from accounts.decorators import role_required
from subjects.models import Subject, Topic

from .models import ExamAttempt
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


@role_required("student")
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
        .select_related("question")
        .order_by("question_order")
    )

    return render(
        request,
        "exams/practice_attempt.html",
        {
            "attempt": attempt,
            "answers": answers,
        },
    )