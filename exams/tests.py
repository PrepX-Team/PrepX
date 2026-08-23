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
from .services.evaluation import (
    calculate_score,
    calculate_accuracy,
    evaluate_answers,
)
import json

from .services.submission import (
    submit_practice_attempt,
    update_student_progress_after_attempt,
)


def make_questions(subject, topic, difficulty, count, admin):
    for i in range(count):
        Question.objects.create(
            subject=subject, topic=topic, question_text=f'Q{i}',
            option_a='a', option_b='b', option_c='c', option_d='d',
            correct_option='A', explanation='e', difficulty_level=difficulty,
            created_by=admin, is_global=True, status='approved',
        )

def build_submitted_attempt(
    student,
    topic,
    admin,
    correct_n,
    wrong_n,
    unanswered_n,
    test_number=1,
):
    """Helper: creates questions, starts an attempt, and sets answer states."""

    make_questions(
        topic.subject,
        topic,
        test_number,
        correct_n + wrong_n + unanswered_n,
        admin,
    )

    client = Client()
    client.force_login(student)

    client.post(
        reverse(
            'practice_start',
            args=[topic.id, test_number],
        )
    )

    attempt = ExamAttempt.objects.get(
        student=student,
        topic=topic,
        test_number=test_number,
    )

    answers = list(
        attempt.answers
        .select_related('question')
        .order_by('question_order')
    )

    i = 0

    # Correct answers
    for _ in range(correct_n):
        answers[i].selected_option = (
            answers[i].question.correct_option
        )
        answers[i].save()
        i += 1

    # Wrong answers
    def wrong_option(correct):
        return next(
            option
            for option in 'ABCD'
            if option != correct
        )

    for _ in range(wrong_n):
        answers[i].selected_option = wrong_option(
            answers[i].question.correct_option
        )
        answers[i].save()
        i += 1

    # Remaining answers intentionally stay unanswered.

    return attempt

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

class EvaluationTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'adme',
            'ae@x.com',
            'pass12345',
            role='admin',
        )

        self.student = User.objects.create_user(
            'stue',
            'se@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='EVAL'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='T',
        )

    def test_all_correct(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            20,
            0,
            0,
        )

        c, i, u = evaluate_answers(attempt)

        self.assertEqual(
            (c, i, u),
            (20, 0, 0),
        )

        self.assertEqual(
            calculate_score(c),
            20,
        )

        self.assertEqual(
            calculate_accuracy(c, 20),
            100.0,
        )

    def test_all_wrong(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            0,
            20,
            0,
        )

        c, i, u = evaluate_answers(attempt)

        self.assertEqual(
            (c, i, u),
            (0, 20, 0),
        )

        self.assertEqual(
            calculate_accuracy(c, 20),
            0.0,
        )

    def test_partial_with_unanswered(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            3,
            2,
        )

        c, i, u = evaluate_answers(attempt)

        self.assertEqual(
            (c, i, u),
            (15, 3, 2),
        )

        self.assertEqual(
            c + i + u,
            20,
        )

        self.assertEqual(
            calculate_accuracy(c, 20),
            75.0,
        )

    def test_zero_answered(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            0,
            0,
            20,
        )

        c, i, u = evaluate_answers(attempt)

        self.assertEqual(
            (c, i, u),
            (0, 0, 20),
        )

        self.assertEqual(
            calculate_accuracy(c, 20),
            0.0,
        )

class SubmissionTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'adms',
            'as@x.com',
            'pass12345',
            role='admin',
        )

        self.student = User.objects.create_user(
            'stus',
            'ss2@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.other = User.objects.create_user(
            'stuo',
            'so@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='SUB'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='T',
        )

        self.client = Client()

    def test_student_can_submit_own_attempt(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            5,
            0,
        )

        self.client.login(
            username='stus',
            password='pass12345',
        )

        response = self.client.post(
            reverse(
                'practice_submit',
                args=[attempt.id],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        attempt.refresh_from_db()

        self.assertEqual(
            attempt.status,
            'submitted',
        )

        self.assertEqual(
            attempt.score,
            15,
        )

        self.assertEqual(
            attempt.accuracy,
            75.0,
        )

    def test_other_student_cannot_submit(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            5,
            0,
        )

        self.client.login(
            username='stuo',
            password='pass12345',
        )

        response = self.client.post(
            reverse(
                'practice_submit',
                args=[attempt.id],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_double_submission_is_idempotent(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            5,
            0,
        )

        submit_practice_attempt(attempt)

        first_end_time = (
            ExamAttempt.objects
            .get(pk=attempt.pk)
            .end_time
        )

        submit_practice_attempt(attempt)

        second_end_time = (
            ExamAttempt.objects
            .get(pk=attempt.pk)
            .end_time
        )

        self.assertEqual(
            first_end_time,
            second_end_time,
        )

    def test_submitted_attempt_answer_save_rejected(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            5,
            0,
        )

        submit_practice_attempt(attempt)

        self.client.login(
            username='stus',
            password='pass12345',
        )

        qid = attempt.answers.first().question_id

        response = self.client.post(
            reverse(
                'practice_answer_save',
                args=[attempt.id],
            ),
            data=json.dumps({
                'question_id': qid,
                'selected_option': 'A',
            }),
            content_type='application/json',
        )

        self.assertEqual(
            response.status_code,
            409,
        )


class ProgressionTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'admp',
            'ap@x.com',
            'pass12345',
            role='admin',
        )

        self.student = User.objects.create_user(
            'stup',
            'sp@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='PROG'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='T',
        )

    def test_74_percent_does_not_unlock(self):
        from students.models import StudentProgress

        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            14,
            6,
            0,
        )

        submit_practice_attempt(attempt)

        progress = StudentProgress.objects.get(
            student=self.student,
            topic=self.topic,
        )

        self.assertEqual(
            progress.highest_unlocked_test,
            1,
        )

    def test_75_percent_unlocks_next(self):
        from students.models import StudentProgress

        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            5,
            0,
        )

        submit_practice_attempt(attempt)

        progress = StudentProgress.objects.get(
            student=self.student,
            topic=self.topic,
        )

        self.assertEqual(
            progress.highest_unlocked_test,
            2,
        )

    def test_progress_never_decreases(self):
        from students.models import StudentProgress

        StudentProgress.objects.create(
            student=self.student,
            topic=self.topic,
            highest_unlocked_test=5,
        )

        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            5,
            15,
            0,
        )

        submit_practice_attempt(attempt)

        progress = StudentProgress.objects.get(
            student=self.student,
            topic=self.topic,
        )

        self.assertEqual(
            progress.highest_unlocked_test,
            5,
        )

    def test_test_10_does_not_unlock_test_11(self):
        from students.models import StudentProgress

        StudentProgress.objects.create(
            student=self.student,
            topic=self.topic,
            highest_unlocked_test=10,
        )

        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            20,
            0,
            0,
            test_number=10,
        )

        submit_practice_attempt(attempt)

        progress = StudentProgress.objects.get(
            student=self.student,
            topic=self.topic,
        )

        self.assertEqual(
            progress.highest_unlocked_test,
            10,
        )


class ResultAccessTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'admr',
            'ar@x.com',
            'pass12345',
            role='admin',
        )

        self.student = User.objects.create_user(
            'stur',
            'sr@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.other = User.objects.create_user(
            'stur2',
            'sr2@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='RES'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='T',
        )

        self.client = Client()

    def test_owner_can_view_result(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            5,
            0,
        )

        submit_practice_attempt(attempt)

        self.client.login(
            username='stur',
            password='pass12345',
        )

        response = self.client.get(
            reverse(
                'practice_result',
                args=[attempt.id],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            '15',
        )

    def test_other_student_cannot_view_result(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            5,
            0,
        )

        submit_practice_attempt(attempt)

        self.client.login(
            username='stur2',
            password='pass12345',
        )

        response = self.client.get(
            reverse(
                'practice_result',
                args=[attempt.id],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_in_progress_attempt_has_no_result(self):
        attempt = build_submitted_attempt(
            self.student,
            self.topic,
            self.admin,
            15,
            5,
            0,
        )

        self.client.login(
            username='stur',
            password='pass12345',
        )

        response = self.client.get(
            reverse(
                'practice_result',
                args=[attempt.id],
            ),
            follow=True,
        )

        self.assertContains(
            response,
            'still in progress',
        )


class TimeoutSubmissionTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'admt2',
            'at2@x.com',
            'pass12345',
            role='admin',
        )

        self.student = User.objects.create_user(
            'stut2',
            'st2@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='TOUT'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='T',
        )

    def test_expired_attempt_auto_finalizes_on_result_view(self):
        make_questions(
            self.subject,
            self.topic,
            1,
            20,
            self.admin,
        )

        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=timezone.now()
            - timezone.timedelta(minutes=31),
            duration=30,
            status='in_progress',
        )

        from exams.services.practice import get_eligible_questions

        for i, q in enumerate(
            get_eligible_questions(
                self.topic,
                1,
            )
        ):
            ExamAnswer.objects.create(
                attempt=attempt,
                question=q,
                question_order=i + 1,
            )

        client = Client()

        client.login(
            username='stut2',
            password='pass12345',
        )

        response = client.get(
            reverse(
                'practice_result',
                args=[attempt.id],
            )
        )

        attempt.refresh_from_db()

        self.assertEqual(
            attempt.status,
            'submitted',
        )

        self.assertIsNotNone(
            attempt.end_time
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_expired_attempt_does_not_reset_timer(self):
        make_questions(
            self.subject,
            self.topic,
            1,
            20,
            self.admin,
        )

        original_start = (
            timezone.now()
            - timezone.timedelta(minutes=31)
        )

        attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=original_start,
            duration=30,
            status='in_progress',
        )

        from exams.services.submission import (
            auto_finalize_if_expired,
        )

        auto_finalize_if_expired(attempt)

        attempt.refresh_from_db()

        self.assertEqual(
            attempt.start_time,
            original_start,
        )

