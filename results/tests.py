from django.test import TestCase
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import User
from subjects.models import Subject, Topic
from exams.models import ExamAttempt

from teachers.models import (
    ConductedExam,
    ConductedExamQuestion,
    ConductedExamParticipant,
)

from .models import Result
from .services import (
    get_or_create_practice_result,
    get_or_create_conducted_result,
)


class ResultModelTests(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username='result_student',
            email='result@example.com',
            password='pass12345',
            role='student',
            is_approved=True,
        )

        self.other_student = User.objects.create_user(
            username='other_student',
            email='other@example.com',
            password='pass12345',
            role='student',
            is_approved=True,
        )

        self.teacher = User.objects.create_user(
            username='result_teacher',
            email='teacher@example.com',
            password='pass12345',
            role='teacher',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='Result Subject'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='Result Topic',
        )

    def test_practice_result_creation(self):
        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=timezone.now(),
            end_time=timezone.now(),
            duration=30,
            score=16,
            accuracy=80.0,
            status='submitted',
        )

        result = get_or_create_practice_result(attempt)

        self.assertIsNotNone(result.pk)
        self.assertEqual(
            result.practice_attempt,
            attempt,
        )
        self.assertIsNone(
            result.conducted_participant,
        )
        self.assertEqual(
            result.student,
            self.student,
        )
        self.assertEqual(
            result.result_type,
            'practice',
        )
        self.assertEqual(
            result.score,
            16,
        )
        self.assertEqual(
            result.accuracy,
            80.0,
        )
        self.assertEqual(
            result.total_marks,
            20,
        )

    def test_practice_result_is_idempotent(self):
        end_time = timezone.now()

        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=end_time,
            end_time=end_time,
            duration=30,
            score=15,
            accuracy=75.0,
            status='submitted',
        )

        first = get_or_create_practice_result(attempt)
        second = get_or_create_practice_result(attempt)

        self.assertEqual(
            first.pk,
            second.pk,
        )

        self.assertEqual(
            Result.objects.filter(
                practice_attempt=attempt
            ).count(),
            1,
        )

    def test_unfinalized_practice_attempt_rejected(self):
        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=timezone.now(),
            status='in_progress',
        )

        with self.assertRaises(ValueError):
            get_or_create_practice_result(attempt)

        self.assertFalse(
            Result.objects.filter(
                practice_attempt=attempt
            ).exists()
        )

    def test_practice_result_requires_end_time(self):
        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=timezone.now(),
            status='submitted',
            score=10,
            accuracy=50.0,
        )

        with self.assertRaises(ValueError):
            get_or_create_practice_result(attempt)

    def test_duplicate_practice_result_blocked(self):
        end_time = timezone.now()

        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=end_time,
            end_time=end_time,
            score=10,
            accuracy=50.0,
            status='submitted',
        )

        get_or_create_practice_result(attempt)

        with self.assertRaises(IntegrityError):
            Result.objects.create(
                practice_attempt=attempt,
                student=self.student,
                finalized_at=end_time,
            )

    def test_result_cannot_have_both_sources(self):
        end_time = timezone.now()

        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=end_time,
            end_time=end_time,
            score=10,
            accuracy=50.0,
            status='submitted',
        )

        conducted_exam = ConductedExam.objects.create(
            teacher=self.teacher,
            exam_name='Both Sources Exam',
            duration_minutes=30,
            negative_marking_enabled=False,
            negative_marks=0,
            status='completed',
        )

        participant = ConductedExamParticipant.objects.create(
            exam=conducted_exam,
            student=self.student,
            status='auto_submitted',
            score=10,
            total_marks=20,
            submitted_at=end_time,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Result.objects.create(
                    practice_attempt=attempt,
                    conducted_participant=participant,
                    student=self.student,
                    finalized_at=end_time,
                )


class ResultServiceConductedTests(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username='conducted_student',
            email='conducted@example.com',
            password='pass12345',
            role='student',
            is_approved=True,
        )

        self.teacher = User.objects.create_user(
            username='conducted_teacher',
            email='conducted_teacher@example.com',
            password='pass12345',
            role='teacher',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='Conducted Subject'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='Conducted Topic',
        )

        self.exam = ConductedExam.objects.create(
            teacher=self.teacher,
            exam_name='Result Conducted Exam',
            duration_minutes=30,
            negative_marking_enabled=False,
            negative_marks=0,
            status='completed',
        )

        self.participant = ConductedExamParticipant.objects.create(
            exam=self.exam,
            student=self.student,
            status='auto_submitted',
            score=16,
            total_marks=20,
            submitted_at=timezone.now(),
        )

    def test_conducted_result_creation(self):
        result = get_or_create_conducted_result(
            self.participant
        )

        self.assertIsNotNone(result.pk)
        self.assertEqual(
            result.conducted_participant,
            self.participant,
        )
        self.assertIsNone(
            result.practice_attempt,
        )
        self.assertEqual(
            result.student,
            self.student,
        )
        self.assertEqual(
            result.result_type,
            'conducted',
        )
        self.assertEqual(
            result.score,
            16,
        )
        self.assertEqual(
            result.total_marks,
            20,
        )
        self.assertEqual(
            result.accuracy,
            80.0,
        )

    def test_conducted_result_is_idempotent(self):
        first = get_or_create_conducted_result(
            self.participant
        )

        second = get_or_create_conducted_result(
            self.participant
        )

        self.assertEqual(
            first.pk,
            second.pk,
        )

        self.assertEqual(
            Result.objects.filter(
                conducted_participant=self.participant
            ).count(),
            1,
        )

    def test_unfinalized_conducted_participant_rejected(self):
        self.participant.status = 'ongoing'
        self.participant.save(
            update_fields=[
                'status',
                'updated_at',
            ]
        )

        with self.assertRaises(ValueError):
            get_or_create_conducted_result(
                self.participant
            )

        self.assertFalse(
            Result.objects.filter(
                conducted_participant=self.participant
            ).exists()
        )

    def test_conducted_result_requires_submission_time(self):
        self.participant.submitted_at = None
        self.participant.save(
            update_fields=[
                'submitted_at',
                'updated_at',
            ]
        )

        with self.assertRaises(ValueError):
            get_or_create_conducted_result(
                self.participant
            )

    def test_duplicate_conducted_result_blocked(self):
        get_or_create_conducted_result(
            self.participant
        )

        with self.assertRaises(IntegrityError):
            Result.objects.create(
                conducted_participant=self.participant,
                student=self.student,
                finalized_at=timezone.now(),
            )

    def test_result_cannot_have_neither_source(self):
        with self.assertRaises(IntegrityError):
            Result.objects.create(
                student=self.student,
                finalized_at=timezone.now(),
            )