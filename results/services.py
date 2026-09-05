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


def _format_duration(duration):
    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    if minutes:
        return f'{minutes} min {seconds:02d} sec'

    return f'{seconds} sec'


def get_conducted_exam_leaderboard(exam):
    participants = list(
        exam.participants.filter(
            status__in=['submitted', 'auto_submitted'],
            started_at__isnull=False,
            submitted_at__isnull=False,
        ).select_related('student')
    )

    participants.sort(
        key=lambda p: (
            -p.score,
            p.submitted_at - p.started_at,
            p.pk,
        )
    )

    return [
        {
            'rank': rank,
            'participant': participant,
            'time_taken': _format_duration(
                participant.submitted_at
                - participant.started_at
            ),
        }
        for rank, participant in enumerate(
            participants,
            start=1,
        )
    ]


def get_conducted_exam_summary(leaderboard):
    if not leaderboard:
        return {
            'students': 0,
            'average_score': 0,
            'highest_score': 0,
            'lowest_score': 0,
        }

    scores = [
        item['participant'].score
        for item in leaderboard
    ]

    return {
        'students': len(scores),
        'average_score': round(
            sum(scores) / len(scores),
            2,
        ),
        'highest_score': max(scores),
        'lowest_score': min(scores),
    }