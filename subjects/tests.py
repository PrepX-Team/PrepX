from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from .models import Subject, Topic


class SubjectTopicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser('adm', 'a@x.com', 'pass12345', role='admin')
        self.teacher = User.objects.create_user('tch', 't@x.com', 'pass12345', role='teacher', is_approved=True)
        self.student = User.objects.create_user('std', 's@x.com', 'pass12345', role='student', is_approved=True)

    def test_admin_can_create_subject(self):
        self.client.login(username='adm', password='pass12345')
        response = self.client.post(reverse('add_subject'), {'name': 'QA'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subject.objects.filter(name='QA').exists())

    def test_teacher_cannot_create_subject(self):
        self.client.login(username='tch', password='pass12345')
        response = self.client.get(reverse('add_subject'))
        self.assertEqual(response.status_code, 403)

    def test_student_cannot_create_subject(self):
        self.client.login(username='std', password='pass12345')
        response = self.client.get(reverse('add_subject'))
        self.assertEqual(response.status_code, 403)

    def test_duplicate_subject_case_insensitive_rejected(self):
        Subject.objects.create(name='QA')
        self.client.login(username='adm', password='pass12345')
        response = self.client.post(reverse('add_subject'), {'name': 'qa'})
        self.assertEqual(Subject.objects.filter(name__iexact='qa').count(), 1)

    def test_duplicate_topic_case_insensitive_rejected(self):
        qa = Subject.objects.create(name='QA')
        Topic.objects.create(subject=qa, name='Average')
        with self.assertRaises(Exception):
            Topic.objects.create(subject=qa, name='average')  # case-insensitive dup

    def test_duplicate_topic_name_different_subject_allowed(self):
        qa = Subject.objects.create(name='QA')
        lr = Subject.objects.create(name='LR')
        Topic.objects.create(subject=qa, name='Puzzles')
        Topic.objects.create(subject=lr, name='Puzzles')  # should succeed — different subjects
        self.assertEqual(Topic.objects.filter(name='Puzzles').count(), 2)