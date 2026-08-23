from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError
from django.utils import timezone
from accounts.models import User
from subjects.models import Subject, Topic
from questions.models import Question
from students.models import StudentProgress
from .models import ExamAttempt, ExamAnswer
from core.constants import QUESTIONS_PER_TEST
from .services.timer import get_remaining_seconds, is_editable


def make_questions(subject, topic, difficulty, count, admin):
    for i in range(count):
        Question.objects.create(
            subject=subject, topic=topic, question_text=f'Q{i}',
            option_a='a', option_b='b', option_c='c', option_d='d',
            correct_option='A', explanation='e', difficulty_level=difficulty,
            created_by=admin, is_global=True, status='approved',
        )


class PracticeAccessTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm', 'a@x.com', 'pass12345', role='admin')
        self.student = User.objects.create_user('stu', 's@x.com', 'pass12345', role='student', is_approved=True)
        self.teacher = User.objects.create_user('tch', 't@x.com', 'pass12345', role='teacher', is_approved=True)
        self.client = Client()

    def test_anonymous_redirected(self):
        response = self.client.get(reverse('practice_home'))
        self.assertEqual(response.status_code, 302)

    def test_student_allowed(self):
        self.client.login(username='stu', password='pass12345')
        response = self.client.get(reverse('practice_home'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_denied(self):
        self.client.login(username='tch', password='pass12345')
        response = self.client.get(reverse('practice_home'))
        self.assertEqual(response.status_code, 403)

    def test_admin_denied(self):
        self.client.login(username='adm', password='pass12345')
        response = self.client.get(reverse('practice_home'))
        self.assertEqual(response.status_code, 403)


class PracticeLockTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm2', 'a2@x.com', 'pass12345', role='admin')
        self.student = User.objects.create_user('stu2', 's2@x.com', 'pass12345', role='student', is_approved=True)
        self.subject = Subject.objects.create(name='QA')
        self.topic = Topic.objects.create(subject=self.subject, name='Average')
        make_questions(self.subject, self.topic, 1, 20, self.admin)
        self.client = Client()
        self.client.login(username='stu2', password='pass12345')

    def test_test1_unlocked_by_default(self):
        response = self.client.post(reverse('practice_start', args=[self.topic.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExamAttempt.objects.filter(student__username='stu2', test_number=1).exists())

    def test_test2_locked_by_default(self):
        response = self.client.post(reverse('practice_start', args=[self.topic.id, 2]), follow=True)
        self.assertFalse(ExamAttempt.objects.filter(student__username='stu2', test_number=2).exists())

    def test_unlocked_up_to_five(self):
        StudentProgress.objects.update_or_create(
            student=self.student, topic=self.topic, defaults={'highest_unlocked_test': 5}
        )
        make_questions(self.subject, self.topic, 5, 20, self.admin)
        response = self.client.post(reverse('practice_start', args=[self.topic.id, 5]))
        self.assertEqual(response.status_code, 302)

    def test_invalid_test_number_rejected(self):
        response = self.client.get(reverse('practice_instructions', args=[self.topic.id, 11]), follow=True)
        self.assertFalse(ExamAttempt.objects.filter(test_number=11).exists())


class QuestionAvailabilityTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm3', 'a3@x.com', 'pass12345', role='admin')
        self.student = User.objects.create_user('stu3', 's3@x.com', 'pass12345', role='student', is_approved=True)
        self.subject = Subject.objects.create(name='LR')
        self.topic = Topic.objects.create(subject=self.subject, name='Puzzles')
        self.client = Client()
        self.client.login(username='stu3', password='pass12345')

    def test_insufficient_questions_blocks_start(self):
        make_questions(self.subject, self.topic, 1, 19, self.admin)  # only 19
        response = self.client.post(reverse('practice_start', args=[self.topic.id, 1]), follow=True)
        self.assertFalse(ExamAttempt.objects.filter(student__username='stu3').exists())

    def test_exactly_twenty_assigned(self):
        make_questions(self.subject, self.topic, 1, 30, self.admin)  # 30 available
        self.client.post(reverse('practice_start', args=[self.topic.id, 1]))
        attempt = ExamAttempt.objects.get(student__username='stu3', test_number=1)
        self.assertEqual(attempt.answers.count(), QUESTIONS_PER_TEST)

    def test_no_duplicate_questions_in_assignment(self):
        make_questions(self.subject, self.topic, 1, 25, self.admin)
        self.client.post(reverse('practice_start', args=[self.topic.id, 1]))
        attempt = ExamAttempt.objects.get(student__username='stu3', test_number=1)
        qids = list(attempt.answers.values_list('question_id', flat=True))
        self.assertEqual(len(qids), len(set(qids)))


class PracticeStabilityAndOwnershipTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('adm4', 'a4@x.com', 'pass12345', role='admin')
        self.student_a = User.objects.create_user('stuA', 'sa@x.com', 'pass12345', role='student', is_approved=True)
        self.student_b = User.objects.create_user('stuB', 'sb@x.com', 'pass12345', role='student', is_approved=True)
        self.subject = Subject.objects.create(name='VA')
        self.topic = Topic.objects.create(subject=self.subject, name='Grammar')
        make_questions(self.subject, self.topic, 1, 20, self.admin)
        self.client = Client()

    def test_question_stability_on_resume(self):
        self.client.login(username='stuA', password='pass12345')
        self.client.post(reverse('practice_start', args=[self.topic.id, 1]))
        attempt1 = ExamAttempt.objects.get(student__username='stuA')
        ids_first = set(attempt1.answers.values_list('question_id', flat=True))

        self.client.post(reverse('practice_start', args=[self.topic.id, 1]))  # resume
        attempt2 = ExamAttempt.objects.get(student__username='stuA')
        ids_second = set(attempt2.answers.values_list('question_id', flat=True))

        self.assertEqual(attempt1.id, attempt2.id)  # same attempt, not a new one
        self.assertEqual(ids_first, ids_second)

    def test_attempt_ownership_enforced(self):
        self.client.login(username='stuA', password='pass12345')
        self.client.post(reverse('practice_start', args=[self.topic.id, 1]))
        attempt = ExamAttempt.objects.get(student__username='stuA')

        self.client.logout()
        self.client.login(username='stuB', password='pass12345')
        response = self.client.get(reverse('practice_attempt', args=[attempt.id]))
        self.assertEqual(response.status_code, 403)

    def test_retake_after_submitted_allowed(self):
        self.client.login(username='stuA', password='pass12345')
        self.client.post(reverse('practice_start', args=[self.topic.id, 1]))
        old = ExamAttempt.objects.get(student__username='stuA')
        old.status = 'submitted'
        old.save()

        self.client.post(reverse('practice_start', args=[self.topic.id, 1]))
        self.assertEqual(ExamAttempt.objects.filter(student__username='stuA').count(), 2)

    def test_duplicate_attempt_question_constraint(self):
        self.client.login(username='stuA', password='pass12345')
        self.client.post(reverse('practice_start', args=[self.topic.id, 1]))
        attempt = ExamAttempt.objects.get(student__username='stuA')
        q = attempt.answers.first().question
        with self.assertRaises(IntegrityError):
            ExamAnswer.objects.create(attempt=attempt, question=q, question_order=99)

class AnswerPersistenceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            'adm5',
            'a5@x.com',
            'pass12345',
            role='admin',
        )

        self.student = User.objects.create_user(
            'stu5',
            's5@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.other = User.objects.create_user(
            'stu6',
            's6@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(name='ANS')
        self.topic = Topic.objects.create(
            subject=self.subject,
            name='T',
        )

        make_questions(
            self.subject,
            self.topic,
            1,
            20,
            self.admin,
        )

        self.client = Client()
        self.client.login(
            username='stu5',
            password='pass12345',
        )

        self.client.post(
            reverse(
                'practice_start',
                args=[self.topic.id, 1],
            )
        )

        self.attempt = ExamAttempt.objects.get(
            student__username='stu5'
        )

        self.qid = (
            self.attempt.answers
            .first()
            .question_id
        )

    def _save(self, question_id, option):
        import json

        return self.client.post(
            reverse(
                'practice_answer_save',
                args=[self.attempt.id],
            ),
            data=json.dumps({
                'question_id': question_id,
                'selected_option': option,
            }),
            content_type='application/json',
        )

    def test_answer_saves_and_updates(self):
        self._save(self.qid, 'A')

        answer = ExamAnswer.objects.get(
            attempt=self.attempt,
            question_id=self.qid,
        )

        self.assertEqual(
            answer.selected_option,
            'A',
        )

        self._save(self.qid, 'C')

        answer.refresh_from_db()

        self.assertEqual(
            answer.selected_option,
            'C',
        )

    def test_invalid_option_rejected(self):
        response = self._save(
            self.qid,
            'Z',
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_unassigned_question_rejected(self):
        other_q = Question.objects.create(
            subject=self.subject,
            topic=self.topic,
            question_text='Other',
            option_a='a',
            option_b='b',
            option_c='c',
            option_d='d',
            correct_option='A',
            explanation='e',
            difficulty_level=1,
            created_by=self.admin,
            is_global=True,
            status='approved',
        )

        response = self._save(
            other_q.id,
            'A',
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_cannot_save_to_other_students_attempt(self):
        self.client.logout()

        self.client.login(
            username='stu6',
            password='pass12345',
        )

        response = self._save(
            self.qid,
            'A',
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_locked_attempt_rejects_save(self):
        self.attempt.status = 'submitted'
        self.attempt.save()

        response = self._save(
            self.qid,
            'A',
        )

        self.assertEqual(
            response.status_code,
            409,
        )

class TimerTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            'adm6',
            'a6@x.com',
            'pass12345',
            role='admin',
        )

        self.student = User.objects.create_user(
            'stu7',
            's7@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='TMR'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='T',
        )

        make_questions(
            self.subject,
            self.topic,
            1,
            20,
            self.admin,
        )

    def test_expired_attempt_has_zero_remaining_time(self):
        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=timezone.now()
            - timezone.timedelta(minutes=31),
            duration=30,
            status='in_progress',
        )

        self.assertEqual(
            get_remaining_seconds(attempt),
            0,
        )

        self.assertFalse(
            is_editable(attempt)
        )

    def test_fresh_attempt_is_editable(self):
        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=timezone.now(),
            duration=30,
            status='in_progress',
        )

        self.assertGreater(
            get_remaining_seconds(attempt),
            0,
        )

        self.assertTrue(
            is_editable(attempt)
        )