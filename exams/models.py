from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint

from core.constants import MIN_TEST_NUMBER, MAX_TEST_NUMBER
from core.models import BaseModel
from subjects.models import Subject, Topic


class Exam(BaseModel):
    """Teacher-created exam — used by the teacher exam system in Phase 4."""

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    title = models.CharField(max_length=200)
    duration = models.IntegerField()
    exam_key = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title


class ExamSection(BaseModel):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,)
    difficulty_level = models.IntegerField()
    number_of_questions = models.IntegerField()


class ExamAttempt(BaseModel):
    """
    Common attempt model for both practice tests and
    future teacher-conducted exams.

    Practice attempt:
        exam = NULL
        topic = selected topic
        test_number = 1-10

    Teacher exam attempt:
        exam = selected exam
        topic = NULL
        test_number = NULL
    """

    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="exam_attempts",)

    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,null=True,blank=True,)

    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,null=True,blank=True,)

    test_number = models.IntegerField(null=True,blank=True,)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True,blank=True,)

    duration = models.IntegerField(null=True,blank=True,help_text="Duration in minutes.",)

    score = models.FloatField(null=True,blank=True,)

    accuracy = models.FloatField(null=True,blank=True,)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="in_progress",)

    class Meta:
        indexes = [
            models.Index(fields=["student"]),
            models.Index(fields=["topic"]),
            models.Index(fields=["status"]),
            models.Index(fields=["test_number"]),
            models.Index(fields=["start_time"]),
        ]
        ordering = ["-start_time"]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.test_number is not None:
            if not (MIN_TEST_NUMBER <= self.test_number <= MAX_TEST_NUMBER):
                raise ValidationError(
                    {
                        "test_number": (
                            f"Test number must be between "
                            f"{MIN_TEST_NUMBER} and {MAX_TEST_NUMBER}."
                        )
                    }
                )

    def __str__(self):
        target = (
            self.topic.name
            if self.topic
            else self.exam.title
            if self.exam
            else "Unknown"
        )

        return (
            f"{self.student.username} - "
            f"{target} - "
            f"{self.status}"
        )


class ExamAnswer(BaseModel):
    """
    Represents a question assigned to an attempt and,
    later, the student's answer to that question.

    At attempt creation:
        selected_option = NULL
        is_correct = NULL

    During/after the test:
        selected_option = student's answer
        is_correct = evaluation result
    """

    OPTION_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]

    attempt = models.ForeignKey(ExamAttempt,on_delete=models.CASCADE,related_name="answers",)

    question = models.ForeignKey("questions.Question",on_delete=models.CASCADE,)

    question_order = models.PositiveSmallIntegerField()

    selected_option = models.CharField(max_length=1,choices=OPTION_CHOICES,null=True,blank=True,)

    is_correct = models.BooleanField(null=True,blank=True,)

    time_spent = models.IntegerField(default=0,help_text="Time spent on the question in seconds.",)

    marked_for_review = models.BooleanField(default=False,)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["attempt", "question"],name="unique_attempt_question",),
            UniqueConstraint(fields=["attempt", "question_order"],name="unique_attempt_question_order",),
        ]
        indexes = [
            models.Index(fields=["attempt"]),
            models.Index(fields=["question"]),
        ]
        ordering = ["attempt", "question_order"]

    def __str__(self):
        return f"Attempt {self.attempt.pk} - Q{self.question_order}"