from django.db import transaction

from .models import Result


def get_or_create_practice_result(attempt):
    """
    Create or retrieve the finalized Result for a
    Phase 3 practice attempt.

    The ExamAttempt remains the authoritative source
    for score and accuracy.
    """

    if attempt.status != 'submitted':
        raise ValueError(
            "Cannot create a Result for an unfinalized attempt."
        )

    if attempt.end_time is None:
        raise ValueError(
            "Cannot create a Result without a finalized end time."
        )

    with transaction.atomic():
        result, _ = Result.objects.get_or_create(
            practice_attempt=attempt,
            defaults={
                'student': attempt.student,
                'finalized_at': attempt.end_time,
            },
        )

    return result


def get_or_create_conducted_result(participant):
    """
    Create or retrieve the finalized Result for a
    Phase 4 conducted-exam participant.

    The ConductedExamParticipant remains the authoritative
    source for score and total marks.
    """

    if participant.status not in (
        'submitted',
        'auto_submitted',
    ):
        raise ValueError(
            "Cannot create a Result for an unfinalized participation."
        )

    if participant.submitted_at is None:
        raise ValueError(
            "Cannot create a Result without a submission time."
        )

    with transaction.atomic():
        result, _ = Result.objects.get_or_create(
            conducted_participant=participant,
            defaults={
                'student': participant.student,
                'finalized_at': participant.submitted_at,
            },
        )

    return result