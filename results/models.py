from django.db import models
from django.db.models import Q, CheckConstraint

from core.models import BaseModel


class Result(BaseModel):
    """
    Unified finalized-result record.

    A Result points to exactly one authoritative source:

    1. Phase 3 practice:
       exams.ExamAttempt

    2. Phase 4 conducted exam:
       teachers.ConductedExamParticipant

    Score and accuracy are NOT duplicated here.
    They are read from the authoritative source.
    """

    practice_attempt = models.OneToOneField(
        'exams.ExamAttempt',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='result',
    )

    conducted_participant = models.OneToOneField(
        'teachers.ConductedExamParticipant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='result',
    )

    student = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='results',
    )

    finalized_at = models.DateTimeField()

    class Meta:
        constraints = [
            CheckConstraint(
                condition=(
                    Q(
                        practice_attempt__isnull=False,
                        conducted_participant__isnull=True,
                    )
                    |
                    Q(
                        practice_attempt__isnull=True,
                        conducted_participant__isnull=False,
                    )
                ),
                name='result_exactly_one_source',
            ),
        ]

        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['finalized_at']),
        ]

        ordering = ['-finalized_at']

    @property
    def result_type(self):
        return (
            'practice'
            if self.practice_attempt_id
            else 'conducted'
        )

    @property
    def score(self):
        if self.practice_attempt_id:
            return self.practice_attempt.score

        return self.conducted_participant.score

    @property
    def total_marks(self):
        if self.practice_attempt_id:
            return 20

        return self.conducted_participant.total_marks

    @property
    def accuracy(self):
        if self.practice_attempt_id:
            return self.practice_attempt.accuracy

        if self.conducted_participant.total_marks:
            return round(
                (
                    self.conducted_participant.score
                    / self.conducted_participant.total_marks
                ) * 100,
                2,
            )

        return 0.0

    def __str__(self):
        return (
            f"Result({self.result_type}) - "
            f"{self.student.username}"
        )