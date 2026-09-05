from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import User
from subjects.models import Subject, Topic
from exams.models import ExamAttempt
from exams.services.submission import submit_practice_attempt

from teachers.models import (
    ConductedExam,
    ConductedExamQuestion,
    ConductedExamParticipant,
)

from .models import Result
from .services import (
    get_or_create_practice_result,
    get_or_create_conducted_result,
    get_conducted_exam_leaderboard,
    get_conducted_exam_summary,
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


class LeaderboardServiceTests(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='leaderboard_teacher',
            email='leaderboard_teacher@example.com',
            password='pass12345',
            role='teacher',
            is_approved=True,
        )

        self.exam = ConductedExam.objects.create(
            teacher=self.teacher,
            exam_name='Leaderboard Exam',
            duration_minutes=30,
            status='completed',
        )

    def create_participant(
        self,
        username,
        score,
        minutes,
        status='submitted',
    ):
        student = User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='pass12345',
            role='student',
            is_approved=True,
        )

        start = timezone.now()

        return ConductedExamParticipant.objects.create(
            exam=self.exam,
            student=student,
            status=status,
            score=score,
            total_marks=20,
            started_at=start,
            submitted_at=start + timezone.timedelta(
                minutes=minutes
            ),
        )

    def test_higher_score_gets_higher_rank(self):
        self.create_participant(
            'student_one',
            score=15,
            minutes=10,
        )
        self.create_participant(
            'student_two',
            score=18,
            minutes=15,
        )

        leaderboard = get_conducted_exam_leaderboard(
            self.exam
        )

        self.assertEqual(
            leaderboard[0]['participant'].score,
            18,
        )

    def test_lower_time_breaks_score_tie(self):
        self.create_participant(
            'student_fast',
            score=18,
            minutes=10,
        )
        self.create_participant(
            'student_slow',
            score=18,
            minutes=15,
        )

        leaderboard = get_conducted_exam_leaderboard(
            self.exam
        )

        self.assertEqual(
            leaderboard[0]['participant']
            .student.username,
            'student_fast',
        )

    def test_unfinished_participant_is_excluded(self):
        self.create_participant(
            'student_done',
            score=15,
            minutes=10,
        )

        self.create_participant(
            'student_ongoing',
            score=20,
            minutes=5,
            status='ongoing',
        )

        leaderboard = get_conducted_exam_leaderboard(
            self.exam
        )

        self.assertEqual(len(leaderboard), 1)
        self.assertEqual(
            leaderboard[0]['participant']
            .student.username,
            'student_done',
        )

    def test_summary_calculates_scores(self):
        self.create_participant(
            'summary_student_one',
            score=10,
            minutes=10,
        )

        self.create_participant(
            'summary_student_two',
            score=18,
            minutes=12,
        )

        leaderboard = get_conducted_exam_leaderboard(
            self.exam
        )

        summary = get_conducted_exam_summary(
            leaderboard
        )

        self.assertEqual(
            summary['students'],
            2,
        )
        self.assertEqual(
            summary['average_score'],
            14,
        )
        self.assertEqual(
            summary['highest_score'],
            18,
        )
        self.assertEqual(
            summary['lowest_score'],
            10,
        )

    def test_summary_handles_empty_leaderboard(self):
        summary = get_conducted_exam_summary([])

        self.assertEqual(
            summary['students'],
            0,
        )
        self.assertEqual(
            summary['average_score'],
            0,
        )
        self.assertEqual(
            summary['highest_score'],
            0,
        )
        self.assertEqual(
            summary['lowest_score'],
            0,
        )


class ResultViewTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='result_view_admin',
            email='result_view_admin@example.com',
            password='pass12345',
            role='admin',
        )

        self.student = User.objects.create_user(
            username='result_view_student',
            email='result_view_student@example.com',
            password='pass12345',
            role='student',
            is_approved=True,
        )

        self.other_student = User.objects.create_user(
            username='result_view_other',
            email='result_view_other@example.com',
            password='pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='Result View Subject'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='Result View Topic',
        )

        # Create the questions required for a practice test.
        for i in range(20):
            from questions.models import Question

            Question.objects.create(
                subject=self.subject,
                topic=self.topic,
                question_text=f'Result View Question {i}',
                option_a='A',
                option_b='B',
                option_c='C',
                option_d='D',
                correct_option='A',
                explanation='Test explanation.',
                difficulty_level=1,
                created_by=self.admin,
                is_global=True,
                status='approved',
            )

        self.client = Client()

    def _create_submitted_result(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse(
                'practice_start',
                args=[self.topic.id, 1],
            )
        )

        self.assertIn(
            response.status_code,
            [200, 302],
        )

        attempt = ExamAttempt.objects.get(
            student=self.student,
            topic=self.topic,
            test_number=1,
        )

        submit_practice_attempt(attempt)

        return Result.objects.get(
            practice_attempt=attempt
        )

    def test_owner_can_view_result_detail(self):
        result = self._create_submitted_result()

        response = self.client.get(
            reverse(
                'result_detail',
                args=[result.id],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'Correct answer'
        )

    def test_other_student_cannot_view_result(self):
        result = self._create_submitted_result()

        self.client.force_login(
            self.other_student
        )

        response = self.client.get(
            reverse(
                'result_detail',
                args=[result.id],
            )
        )

        # Ownership is enforced by the queryset.
        # An inaccessible result is intentionally returned as 404.
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_result_appears_in_result_list(self):
        result = self._create_submitted_result()

        response = self.client.get(
            reverse('result_list')
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'Practice Test 1'
        )

        self.assertContains(
            response,
            'View Result'
        )

    def test_other_student_does_not_see_result_in_list(self):
        self._create_submitted_result()

        self.client.force_login(
            self.other_student
        )

        response = self.client.get(
            reverse('result_list')
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'No results yet'
        )

    def test_empty_result_list(self):
        self.client.force_login(
            self.student
        )

        response = self.client.get(
            reverse('result_list')
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'No results yet'
        )

    def test_question_wise_result_shows_correct_incorrect_unanswered(self):
        self.client.force_login(self.student)

        self.client.post(
            reverse(
                'practice_start',
                args=[self.topic.id, 1],
            )
        )

        attempt = ExamAttempt.objects.get(
            student=self.student,
            topic=self.topic,
            test_number=1,
        )

        answers = list(
            attempt.answers
            .select_related('question')
            .order_by('question_order')
        )

        # Question 1: correct
        answers[0].selected_option = (
            answers[0].question.correct_option
        )
        answers[0].save()

        # Question 2: incorrect
        wrong_option = next(
            option
            for option in 'ABCD'
            if option != answers[1].question.correct_option
        )

        answers[1].selected_option = wrong_option
        answers[1].save()

        # Question 3 remains unanswered.

        submit_practice_attempt(attempt)

        result = Result.objects.get(
            practice_attempt=attempt
        )

        response = self.client.get(
            reverse(
                'result_detail',
                args=[result.id],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'Correct'
        )

        self.assertContains(
            response,
            'Incorrect'
        )

        self.assertContains(
            response,
            'Unanswered'
        )