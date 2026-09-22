from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import User
from subjects.models import Subject, Topic
from exams.models import ExamAttempt
from .models import Certificate
from .services import issue_if_eligible


class CertificateTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='certstudent', password='TestPass123!', role='student')
        self.other = User.objects.create_user(username='otherstudent', password='TestPass123!', role='student')
        self.subject = Subject.objects.create(name='Certificate subject')
        self.topic = Topic.objects.create(subject=self.subject, name='Certificate topic')

    def complete(self, number, student=None):
        now = timezone.now()
        return ExamAttempt.objects.create(student=student or self.student, topic=self.topic,
            test_number=number, exam=None, status='submitted', start_time=now-timedelta(minutes=5),
            end_time=now, score=20, accuracy=100)

    def test_requires_all_ten_distinct_tests(self):
        for number in range(1, 10):
            self.complete(number)
        self.assertFalse(Certificate.objects.filter(student=self.student).exists())
        self.assertIsNone(issue_if_eligible(self.student, self.topic))
        self.complete(10)
        self.assertEqual(Certificate.objects.filter(student=self.student, topic=self.topic).count(), 1)

    def test_duplicate_attempts_do_not_issue_extra_certificates(self):
        for number in range(1, 11):
            self.complete(number)
        self.complete(10)
        issue_if_eligible(self.student, self.topic)
        self.assertEqual(Certificate.objects.filter(student=self.student, topic=self.topic).count(), 1)

    def test_pdf_private_verification_public(self):
        for number in range(1, 11):
            self.complete(number)
        certificate = Certificate.objects.get(student=self.student, topic=self.topic)
        url = reverse('certificate_pdf', args=[certificate.certificate_id])
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.student)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b'%PDF'))
        self.client.logout()
        self.assertEqual(self.client.get(reverse('certificate_verify', args=[certificate.certificate_id])).status_code, 200)

    def test_conducted_exams_do_not_qualify(self):
        for number in range(1, 10):
            self.complete(number)
        self.assertIsNone(issue_if_eligible(self.student, self.topic))


class CertificateQRTests(TestCase):
    def test_qr_contains_correct_public_verification_url(self):
        from unittest.mock import patch

        student = User.objects.create_user(
            username='qrstudent',
            password='TestPass123!',
            role='student',
        )
        subject = Subject.objects.create(name='QR Test Subject')
        topic = Topic.objects.create(
            subject=subject,
            name='QR Test Topic',
        )
        certificate = Certificate.objects.create(
            student=student,
            topic=topic,
            completed_at=timezone.now(),
        )

        verify_url = reverse(
            'certificate_verify',
            args=[certificate.certificate_id],
        )
        pdf_url = reverse(
            'certificate_pdf',
            args=[certificate.certificate_id],
        )

        self.client.force_login(student)

        with patch('certificates.views.draw_qr') as qr_mock:
            response = self.client.get(pdf_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b'%PDF'))

        expected_url = (
            'http://testserver' + verify_url
        )

        qr_mock.assert_called_once()
        self.assertEqual(
            qr_mock.call_args.args[1],
            expected_url,
        )

        self.client.logout()

        verification_response = self.client.get(verify_url)

        self.assertEqual(
            verification_response.status_code,
            200,
        )
        self.assertEqual(
            verification_response.context['certificate'].pk,
            certificate.pk,
        )
