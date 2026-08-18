from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from subjects.models import Subject, Topic

from .models import Question


class QuestionOwnershipTests(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(
            name='QA'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='Averages'
        )

        self.teacher_a = User.objects.create_user(
            'teacherA',
            'a@x.com',
            'ComplexPass123',
            role='teacher',
            is_approved=True
        )

        self.teacher_b = User.objects.create_user(
            'teacherB',
            'b@x.com',
            'ComplexPass123',
            role='teacher',
            is_approved=True
        )

        self.question = Question.objects.create(
            subject=self.subject,
            topic=self.topic,
            question_text='Q1',
            option_a='a',
            option_b='b',
            option_c='c',
            option_d='d',
            correct_option='A',
            explanation='exp',
            difficulty_level=1,
            created_by=self.teacher_a,
            is_global=False,
        )

        self.client = Client()

    def test_teacher_b_cannot_edit_teacher_a_question(self):
        self.client.login(
            username='teacherB',
            password='ComplexPass123'
        )

        response = self.client.get(
            reverse(
                'edit_question',
                args=[self.question.pk]
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_teacher_b_does_not_see_teacher_a_private_question(self):
        self.client.login(
            username='teacherB',
            password='ComplexPass123'
        )

        response = self.client.get(
            reverse('question_list')
        )

        self.assertNotContains(
            response,
            'Q1'
        )

    def test_difficulty_out_of_range_rejected(self):
        from .forms import QuestionForm

        form = QuestionForm(
            data={
                'subject': self.subject.id,
                'topic': self.topic.id,
                'question_text': 'Bad',
                'option_a': 'a',
                'option_b': 'b',
                'option_c': 'c',
                'option_d': 'd',
                'correct_option': 'A',
                'explanation': 'e',
                'difficulty_level': 15,
            }
        )

        self.assertFalse(form.is_valid())

    def test_topic_must_belong_to_subject(self):
        other_subject = Subject.objects.create(
            name='LR'
        )

        other_topic = Topic.objects.create(
            subject=other_subject,
            name='Puzzles'
        )

        from .forms import QuestionForm

        form = QuestionForm(
            data={
                'subject': self.subject.id,
                'topic': other_topic.id,
                'question_text': 'Bad',
                'option_a': 'a',
                'option_b': 'b',
                'option_c': 'c',
                'option_d': 'd',
                'correct_option': 'A',
                'explanation': 'e',
                'difficulty_level': 5,
            }
        )

        self.assertFalse(form.is_valid())


class QuestionFilterTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name='QA')
        self.topic = Topic.objects.create(subject=self.subject, name='Average')
        self.admin = User.objects.create_superuser('adm2', 'a2@x.com', 'pass12345', role='admin')
        Question.objects.create(
            subject=self.subject, topic=self.topic, question_text='Find average speed',
            option_a='a', option_b='b', option_c='c', option_d='d',
            correct_option='A', explanation='exp', difficulty_level=3,
            created_by=self.admin, is_global=True, status='approved',
        )
        self.client = Client()
        self.client.login(username='adm2', password='pass12345')

    def test_search_filter(self):
        response = self.client.get(reverse('question_list'), {'search': 'average speed'})
        self.assertContains(response, 'Find average speed')

    def test_difficulty_filter_excludes_others(self):
        response = self.client.get(reverse('question_list'), {'difficulty': 7})
        self.assertNotContains(response, 'Find average speed')

    def test_pagination_works(self):
        for i in range(15):
            Question.objects.create(
                subject=self.subject, topic=self.topic, question_text=f'Q{i}',
                option_a='a', option_b='b', option_c='c', option_d='d',
                correct_option='A', explanation='e', difficulty_level=1,
                created_by=self.admin, is_global=True, status='approved',
            )
        response = self.client.get(reverse('question_list'))
        self.assertEqual(len(response.context['page_obj']), 10)


class QuestionDetailSecurityTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name='QA')
        self.topic = Topic.objects.create(subject=self.subject, name='Average')
        self.teacher_a = User.objects.create_user('tA', 'ta@x.com', 'pass12345', role='teacher', is_approved=True)
        self.teacher_b = User.objects.create_user('tB', 'tb@x.com', 'pass12345', role='teacher', is_approved=True)
        self.student = User.objects.create_user('stu', 'stu@x.com', 'pass12345', role='student', is_approved=True)
        self.private_q = Question.objects.create(
            subject=self.subject, topic=self.topic, question_text='Private Q',
            option_a='a', option_b='b', option_c='c', option_d='d',
            correct_option='A', explanation='exp', difficulty_level=2,
            created_by=self.teacher_a, is_global=False, status='pending',
        )
        self.client = Client()

    def test_teacher_b_cannot_view_teacher_a_detail_directly(self):
        self.client.login(username='tB', password='pass12345')
        response = self.client.get(reverse('question_detail', args=[self.private_q.pk]))
        self.assertEqual(response.status_code, 403)

    def test_student_cannot_view_pending_private_question(self):
        self.client.login(username='stu', password='pass12345')
        response = self.client.get(reverse('question_detail', args=[self.private_q.pk]))
        self.assertEqual(response.status_code, 403)

    def test_student_does_not_see_correct_answer_on_visible_question(self):
        self.private_q.is_global = True
        self.private_q.status = 'approved'
        self.private_q.save()
        self.client.login(username='stu', password='pass12345')
        response = self.client.get(reverse('question_detail', args=[self.private_q.pk]))
        self.assertNotContains(response, 'Correct Answer')