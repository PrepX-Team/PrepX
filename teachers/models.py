from django.db import models
from django.conf import settings
from core.models import BaseModel


class ConductedExam(BaseModel):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conducted_exams',
        limit_choices_to={'role': 'teacher'},
    )

    exam_name = models.CharField(max_length=200)

    duration_minutes = models.PositiveIntegerField()

    negative_marking_enabled = models.BooleanField(default=False)

    negative_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    exam_key = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    ends_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.exam_name



class ConductedExamQuestion(BaseModel):

    exam = models.ForeignKey(
        ConductedExam,
        on_delete=models.CASCADE,
        related_name='exam_questions',
    )

    question = models.ForeignKey(
        'questions.Question',
        on_delete=models.PROTECT,
        related_name='conducted_exam_questions',
    )

    marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    question_order = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['exam', 'question'],
                name='unique_question_per_conducted_exam',
            ),
            models.UniqueConstraint(
                fields=['exam', 'question_order'],
                name='unique_question_order_per_conducted_exam',
            ),
        ]

        ordering = ['question_order']

    def __str__(self):
        return f"{self.exam.exam_name} - Question {self.question_order}"

class ConductedExamParticipant(BaseModel):

    STATUS_CHOICES = [
        ('joined', 'Joined'),
        ('ongoing', 'Ongoing'),
        ('submitted', 'Submitted'),
        ('auto_submitted', 'Auto Submitted'),
    ]

    exam = models.ForeignKey(
        ConductedExam,
        on_delete=models.CASCADE,
        related_name='participants',
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conducted_exam_participations',
        limit_choices_to={'role': 'student'},
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='joined',
    )

    score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    total_marks = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    violation_count = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['exam', 'student'],
                name='unique_student_per_conducted_exam',
            ),
        ]

        indexes = [
            models.Index(fields=['exam', 'status']),
            models.Index(fields=['student', 'status']),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.exam.exam_name}"

class ConductedExamAnswer(BaseModel):

    participant = models.ForeignKey(
        ConductedExamParticipant,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    exam_question = models.ForeignKey(
        ConductedExamQuestion,
        on_delete=models.PROTECT,
        related_name='student_answers',
    )

    selected_option = models.CharField(
        max_length=1,
        blank=True,
        null=True,
    )

    answered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_correct = models.BooleanField(
        null=True,
        blank=True,
    )

    marks_obtained = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['participant', 'exam_question'],
                name='unique_answer_per_participant_question',
            ),
        ]

        indexes = [
            models.Index(
                fields=['participant', 'exam_question']
            ),
        ]

    def __str__(self):
        return (
            f"{self.participant.student.username} - "
            f"Q{self.exam_question.question_order}"
        )