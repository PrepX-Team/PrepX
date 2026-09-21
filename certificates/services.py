"""Certificate rules: complete practice tests 1 to 10 for one topic."""

from django.db.models import Max

from core.constants import MIN_TEST_NUMBER, MAX_TEST_NUMBER
from exams.models import ExamAttempt
from subjects.models import Topic
from .models import Certificate


def eligible_completion(student, topic):
    """Return completion date only when every required test was submitted."""
    attempts = ExamAttempt.objects.filter(
        student=student,
        topic=topic,
        exam__isnull=True,
        status='submitted',
        end_time__isnull=False,
        test_number__gte=MIN_TEST_NUMBER,
        test_number__lte=MAX_TEST_NUMBER,
    )
    dates = dict(
        attempts.values('test_number')
        .annotate(completed_at=Max('end_time'))
        .values_list('test_number', 'completed_at')
    )
    required_tests = range(MIN_TEST_NUMBER, MAX_TEST_NUMBER + 1)
    if not all(number in dates for number in required_tests):
        return None
    return max(dates.values())


def issue_if_eligible(student, topic):
    completed_at = eligible_completion(student, topic)
    if completed_at is None:
        return None

    certificate, created = Certificate.objects.get_or_create(
        student=student,
        topic=topic,
        defaults={'completed_at': completed_at},
    )
    return certificate


def sync_student_certificates(student):
    """Check earlier completed practice tests when student opens Certificates."""
    topic_ids = ExamAttempt.objects.filter(
        student=student,
        exam__isnull=True,
        status='submitted',
        topic__isnull=False,
    ).values_list('topic_id', flat=True).distinct()

    for topic in Topic.objects.filter(id__in=topic_ids):
        issue_if_eligible(student, topic)
