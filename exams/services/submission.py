from django.db import transaction
from django.utils import timezone

from core.constants import UNLOCK_PERCENTAGE, MAX_TEST_NUMBER
from .evaluation import (
    evaluate_answers,
    calculate_score,
    calculate_accuracy,
)
from .timer import is_expired


class SubmissionError(Exception):
    """Raised when a practice attempt cannot be submitted."""
    pass


def update_student_progress_after_attempt(attempt):
    """
    Unlock the next practice test when the student achieves the
    required percentage.

    Progress is monotonic: an existing unlocked test is never locked
    again by a later lower-scoring attempt.
    """
    from students.models import StudentProgress

    if (
        attempt.accuracy is None
        or attempt.accuracy < UNLOCK_PERCENTAGE
        or attempt.test_number is None
        or attempt.topic_id is None
    ):
        return

    progress, _ = StudentProgress.objects.get_or_create(
        student=attempt.student,
        topic=attempt.topic,
        defaults={'highest_unlocked_test': 1},
    )

    next_test = min(
        attempt.test_number + 1,
        MAX_TEST_NUMBER,
    )

    if next_test > progress.highest_unlocked_test:
        progress.highest_unlocked_test = next_test
        progress.save(
            update_fields=['highest_unlocked_test']
        )


def submit_practice_attempt(attempt):
    """
    Finalize a practice attempt.

    All result data is calculated server-side from the persisted
    ExamAnswer and Question records.

    The operation is idempotent: submitting an already-submitted
    attempt returns the existing finalized attempt.
    """
    with transaction.atomic():

        locked = (
            type(attempt)
            .objects
            .select_for_update()
            .select_related('student', 'topic')
            .get(pk=attempt.pk)
        )

        # Ensure this service is only used for practice attempts.
        if (
            locked.topic_id is None
            or locked.test_number is None
        ):
            raise SubmissionError(
                "This is not a practice attempt."
            )

        # Idempotent submission.
        if locked.status == 'submitted':
            return locked

        # Only an in-progress attempt can be finalized.
        if locked.status != 'in_progress':
            raise SubmissionError(
                "This attempt cannot be submitted."
            )

        correct, incorrect, unanswered = evaluate_answers(
            locked
        )

        total = correct + incorrect + unanswered

        locked.score = calculate_score(correct)

        locked.accuracy = calculate_accuracy(
            correct,
            total,
        )

        locked.end_time = timezone.now()
        locked.status = 'submitted'

        locked.save(
            update_fields=[
                'score',
                'accuracy',
                'end_time',
                'status',
            ]
        )

        update_student_progress_after_attempt(
            locked
        )

    return locked


def auto_finalize_if_expired(attempt):
    """
    Finalize an in-progress practice attempt if its
    server-authoritative timer has expired.
    """
    if (
        attempt.status == 'in_progress'
        and is_expired(attempt)
    ):
        return submit_practice_attempt(attempt)

    return attempt