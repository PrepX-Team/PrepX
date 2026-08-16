from django.test import TestCase, Client
from django.urls import reverse

from .models import User


class AuthTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_superuser(
            'admin1',
            'a@x.com',
            'pass12345',
            role='admin'
        )

    def test_student_registration(self):
        response = self.client.post(
            reverse('register_student'),
            {
                'first_name': 'Test',
                'last_name': 'Student',
                'username': 'stud1',
                'email': 'stud1@x.com',
                'password1': 'ComplexPass123',
                'password2': 'ComplexPass123',
            }
        )

        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username='stud1')

        self.assertEqual(user.role, 'student')
        self.assertTrue(user.is_approved)

    def test_teacher_registration_requires_approval(self):
        response = self.client.post(
            reverse('register_teacher'),
            {
                'first_name': 'Test',
                'last_name': 'Teacher',
                'username': 'teach1',
                'email': 'teach1@x.com',
                'password1': 'ComplexPass123',
                'password2': 'ComplexPass123',
            }
        )

        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username='teach1')

        self.assertEqual(user.role, 'teacher')
        self.assertFalse(user.is_approved)

    def test_unapproved_teacher_cannot_login(self):
        User.objects.create_user(
            'teach2',
            'teach2@x.com',
            'ComplexPass123',
            role='teacher',
            is_approved=False
        )

        response = self.client.post(
            reverse('login'),
            {
                'username': 'teach2',
                'password': 'ComplexPass123'
            }
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_student_cannot_access_admin_dashboard(self):
        User.objects.create_user(
            'stud2',
            'stud2@x.com',
            'ComplexPass123',
            role='student',
            is_approved=True
        )

        self.client.login(
            username='stud2',
            password='ComplexPass123'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_admin_dashboard(self):
        User.objects.create_user(
            'teach3',
            'teach3@x.com',
            'ComplexPass123',
            role='teacher',
            is_approved=True
        )

        self.client.login(
            username='teach3',
            password='ComplexPass123'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_access_admin_dashboard(self):
        self.client.login(
            username='admin1',
            password='pass12345'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 200)