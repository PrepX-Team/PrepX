from django.utils import timezone
from django.db import transaction
from django.db.models import Q

from questions.models import Question
from students.models import StudentProgress
from core.constants import (
    QUESTIONS_PER_TEST,
    MIN_TEST_NUMBER,
    MAX_TEST_NUMBER,
    DEFAULT_PRACTICE_DURATION_MINUTES,
)
from ..models import ExamAttempt, ExamAnswer


class PracticeError(Exception):
    """Raised for any validation failure in the practice-start flow."""

    pass


def get_eligible_questions(topic, test_number):
    """Return student-visible questions eligible for a practice test."""

    return Question.objects.filter(
        topic=topic,
        difficulty_level=test_number,
        is_global=True,
        status="approved",
        is_active=True,
    )


def get_unlocked_test_number(student, topic):
    progress, _ = StudentProgress.objects.get_or_create(
        student=student,
        topic=topic,
        defaults={"highest_unlocked_test": 1},
    )

    return progress.highest_unlocked_test


def start_practice_attempt(student, topic, test_number):
    if not (MIN_TEST_NUMBER <= test_number <= MAX_TEST_NUMBER):
        raise PracticeError("Invalid test number.")

    if not topic.is_active or not topic.subject.is_active:
        raise PracticeError("This topic is not currently available.")

    unlocked = get_unlocked_test_number(student, topic)

    if test_number > unlocked:
        raise PracticeError("This test is currently locked.")

    # Resume an existing in-progress attempt instead of creating a duplicate.
    existing = ExamAttempt.objects.filter(
        student=student,
        topic=topic,
        test_number=test_number,
        status="in_progress",
    ).first()

    if existing:
        return existing

    eligible = list(
        get_eligible_questions(topic, test_number)
    )

    if len(eligible) < QUESTIONS_PER_TEST:
        raise PracticeError(
            "This test is not available yet because fewer than "
            f"{QUESTIONS_PER_TEST} eligible questions exist."
        )

    import random

    selected = random.sample(
        eligible,
        QUESTIONS_PER_TEST,
    )

    with transaction.atomic():
        attempt = ExamAttempt.objects.create(
            student=student,
            topic=topic,
            test_number=test_number,
            start_time=timezone.now(),
            duration=DEFAULT_PRACTICE_DURATION_MINUTES,
            status='in_progress',
        )

        ExamAnswer.objects.bulk_create(
            [
                ExamAnswer(
                    attempt=attempt,
                    question=question,
                    question_order=index + 1,
                )
                for index, question in enumerate(selected)
            ]
        )

    return attempt