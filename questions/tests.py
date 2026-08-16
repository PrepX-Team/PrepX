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