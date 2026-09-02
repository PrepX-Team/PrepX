from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from subjects.models import Subject, Topic
from questions.models import Question
from exams.models import ExamAttempt, ExamAnswer, Exam

from . import services


class StudentAnalyticsTests(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username='analytics_student',
            email='analytics@example.com',
            password='pass12345',
            role='student',
            is_approved=True,
        )

        self.admin = User.objects.create_superuser(
            username='analytics_admin',
            email='analytics_admin@example.com',
            password='pass12345',
            role='admin',
        )

        self.subject = Subject.objects.create(
            name='Analytics Subject'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='Analytics Topic',
        )

    def create_attempt(
        self,
        score=15,
        accuracy=75.0,
        status='submitted',
        exam=None,
        test_number=1,
        start_time=None,
        end_time=None,
    ):
        start_time = start_time or timezone.now()
        end_time = end_time or start_time

        return ExamAttempt.objects.create(
            student=self.student,
            exam=exam,
            topic=self.topic,
            test_number=test_number,
            start_time=start_time,
            end_time=end_time,
            duration=30,
            status=status,
            score=score,
            accuracy=accuracy,
        )

    def test_no_data_returns_has_data_false(self):
        result = services.student_overview(
            self.student
        )

        self.assertFalse(
            result['has_data']
        )

    def test_zero_attempts_no_crash_on_trend(self):
        result = services.trend(
            self.student
        )

        self.assertEqual(
            result['status'],
            'insufficient_data',
        )

    def test_overview_aggregates_correctly(self):
        self.create_attempt(
            score=15,
            accuracy=75.0,
        )

        self.create_attempt(
            score=10,
            accuracy=50.0,
        )

        overview = services.student_overview(
            self.student
        )

        self.assertTrue(
            overview['has_data']
        )

        self.assertEqual(
            overview['completed_tests'],
            2,
        )

        self.assertEqual(
            overview['average_score'],
            12.5,
        )

        self.assertEqual(
            overview['overall_accuracy'],
            62.5,
        )

    def test_overview_counts_answer_statuses(self):
        attempt = self.create_attempt(
            score=10,
            accuracy=50.0,
        )

        # Create three answers:
        # 1 correct
        # 1 incorrect
        # 1 unanswered

        question_data = []

        for index in range(3):
            question = Question.objects.create(
                subject=self.subject,
                topic=self.topic,
                question_text=f'Analytics Question {index}',
                option_a='A',
                option_b='B',
                option_c='C',
                option_d='D',
                correct_option='A',
                explanation='Explanation',
                difficulty_level=1,
                created_by=self.admin,
                is_global=True,
                status='approved',
            )

            question_data.append(question)

        ExamAnswer.objects.create(
            attempt=attempt,
            question=question_data[0],
            question_order=1,
            selected_option='A',
            is_correct=True,
        )

        ExamAnswer.objects.create(
            attempt=attempt,
            question=question_data[1],
            question_order=2,
            selected_option='B',
            is_correct=False,
        )

        ExamAnswer.objects.create(
            attempt=attempt,
            question=question_data[2],
            question_order=3,
            selected_option=None,
            is_correct=False,
        )

        overview = services.student_overview(
            self.student
        )

        self.assertEqual(
            overview['correct'],
            1,
        )

        self.assertEqual(
            overview['incorrect'],
            1,
        )

        self.assertEqual(
            overview['unanswered'],
            1,
        )

    def test_only_submitted_attempts_are_counted(self):
        self.create_attempt(
            score=15,
            accuracy=75.0,
            status='submitted',
        )

        self.create_attempt(
            score=20,
            accuracy=100.0,
            status='in_progress',
        )

        overview = services.student_overview(
            self.student
        )

        self.assertEqual(
            overview['completed_tests'],
            1,
        )

        self.assertEqual(
            overview['average_score'],
            15.0,
        )

    def test_non_practice_exam_attempts_are_excluded(self):
        exam = Exam.objects.create(
            teacher=self.admin,
            title='Analytics Non-Practice Exam',
            duration=30,
            exam_key='ANALYTICS-NON-PRACTICE',
        )

        self.create_attempt(
            score=10,
            accuracy=50.0,
            exam=None,
        )

        self.create_attempt(
            score=20,
            accuracy=100.0,
            exam=exam,
        )

        overview = services.student_overview(self.student)

        self.assertEqual(overview['completed_tests'], 1)
        self.assertEqual(overview['average_score'], 10.0)
        self.assertEqual(overview['overall_accuracy'], 50.0)

    def test_topic_analytics_requires_minimum_attempts(self):
        for _ in range(4):
            self.create_attempt(
                score=10,
                accuracy=50.0,
            )

        topics = services.topic_analytics(
            self.student
        )

        self.assertEqual(
            len(topics),
            1,
        )

        self.assertEqual(
            topics[0]['attempts'],
            4,
        )

        self.assertFalse(
            topics[0]['sufficient_data']
        )

        # Fifth attempt reaches the analytics threshold.
        self.create_attempt(
            score=10,
            accuracy=50.0,
        )

        topics = services.topic_analytics(
            self.student
        )

        self.assertTrue(
            topics[0]['sufficient_data']
        )

    def test_weak_and_strong_topics_require_sufficient_data(self):
        for _ in range(4):
            self.create_attempt(
                score=5,
                accuracy=25.0,
            )

        result = services.weak_strong_topics(
            self.student
        )

        self.assertEqual(
            result['weak'],
            [],
        )

        # Fifth attempt makes the topic eligible.
        self.create_attempt(
            score=5,
            accuracy=25.0,
        )

        result = services.weak_strong_topics(
            self.student
        )

        self.assertEqual(
            len(result['weak']),
            1,
        )

        self.assertEqual(
            result['weak'][0]['accuracy'],
            25.0,
        )

    def test_difficulty_analytics(self):
        self.create_attempt(
            score=10,
            accuracy=50.0,
            test_number=1,
        )

        self.create_attempt(
            score=18,
            accuracy=90.0,
            test_number=5,
        )

        difficulty = services.difficulty_analytics(
            self.student
        )

        self.assertEqual(
            len(difficulty),
            2,
        )

        self.assertEqual(
            difficulty[0]['difficulty'],
            1,
        )

        self.assertEqual(
            difficulty[0]['accuracy'],
            50.0,
        )

        self.assertEqual(
            difficulty[1]['difficulty'],
            5,
        )

        self.assertEqual(
            difficulty[1]['accuracy'],
            90.0,
        )

    def test_time_analytics(self):
        start = timezone.now()

        self.create_attempt(
            start_time=start,
            end_time=start + timezone.timedelta(
                seconds=60
            ),
        )

        self.create_attempt(
            start_time=start,
            end_time=start + timezone.timedelta(
                seconds=120
            ),
        )

        result = services.time_analytics(
            self.student
        )

        self.assertTrue(
            result['has_data']
        )

        self.assertEqual(
            result['average_time_seconds'],
            90.0,
        )

        self.assertEqual(
            result['total_tests'],
            2,
        )

    def test_trend_requires_ten_completed_practice_attempts(self):
        for _ in range(9):
            self.create_attempt(
                accuracy=70.0,
            )

        result = services.trend(
            self.student
        )

        self.assertEqual(
            result['status'],
            'insufficient_data',
        )

    def test_trend_is_improving(self):
        # Previous five = 60%
        for _ in range(5):
            self.create_attempt(
                accuracy=60.0,
            )

        # Recent five = 80%
        for _ in range(5):
            self.create_attempt(
                accuracy=80.0,
            )

        result = services.trend(
            self.student
        )

        self.assertEqual(
            result['status'],
            'improving',
        )

        self.assertEqual(
            result['recent_avg'],
            80.0,
        )

        self.assertEqual(
            result['previous_avg'],
            60.0,
        )

    def test_trend_is_declining(self):
        # Previous five = 80%
        for _ in range(5):
            self.create_attempt(
                accuracy=80.0,
            )

        # Recent five = 60%
        for _ in range(5):
            self.create_attempt(
                accuracy=60.0,
            )

        result = services.trend(
            self.student
        )

        self.assertEqual(
            result['status'],
            'declining',
        )

    def test_trend_is_stable_within_threshold(self):
        # Previous five = 70%
        for _ in range(5):
            self.create_attempt(
                accuracy=70.0,
            )

        # Recent five = 74%
        # Difference = +4 percentage points.
        for _ in range(5):
            self.create_attempt(
                accuracy=74.0,
            )

        result = services.trend(
            self.student
        )

        self.assertEqual(
            result['status'],
            'stable',
        )