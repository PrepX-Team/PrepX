from django.utils import timezone

from core.constants import DEFAULT_PRACTICE_DURATION_MINUTES


def get_remaining_seconds(attempt):
    """Return server-authoritative remaining time for an attempt."""

    if attempt.status != "in_progress":
        return 0

    duration_minutes = (
        attempt.duration
        or DEFAULT_PRACTICE_DURATION_MINUTES
    )

    deadline = attempt.start_time + timezone.timedelta(
        minutes=duration_minutes
    )

    remaining = (
        deadline - timezone.now()
    ).total_seconds()

    return max(0, int(remaining))


def is_expired(attempt):
    return (
        attempt.status == "in_progress"
        and get_remaining_seconds(attempt) <= 0
    )


def is_editable(attempt):
    """Return whether the attempt can accept answer/review updates."""

    return (
        attempt.status == "in_progress"
        and not is_expired(attempt)
    )