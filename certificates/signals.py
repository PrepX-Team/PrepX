from django.db.models.signals import post_save
from django.dispatch import receiver
from exams.models import ExamAttempt
from .services import issue_if_eligible


@receiver(post_save, sender=ExamAttempt)
def issue_certificate_after_practice(sender, instance, **kwargs):
    if (instance.status == 'submitted' and instance.exam_id is None and
            instance.topic_id and instance.test_number is not None and instance.end_time):
        issue_if_eligible(instance.student, instance.topic)
