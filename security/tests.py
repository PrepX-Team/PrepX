import json

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from subjects.models import Subject, Topic
from exams.models import ExamAttempt

from .models import ExamLog


class SecurityEventTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            'stuS',
            'ss@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.other = User.objects.create_user(
            'stuT',
            'st@x.com',
            'pass12345',
            role='student',
            is_approved=True,
        )

        self.subject = Subject.objects.create(
            name='SEC'
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            name='T',
        )

        self.attempt = ExamAttempt.objects.create(
            student=self.student,
            topic=self.topic,
            test_number=1,
            start_time=timezone.now(),
            duration=30,
            status='in_progress',
        )

        self.client = Client()

        self.client.login(
            username='stuS',
            password='pass12345',
        )

    def _log(self, event_type):
        return self.client.post(
            reverse(
                'log_security_event',
                args=[self.attempt.id],
            ),
            data=json.dumps({
                'event_type': event_type,
            }),
            content_type='application/json',
        )

    def test_valid_event_logged(self):
        response = self._log('tab_switch')

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            ExamLog.objects.filter(
                attempt=self.attempt,
                event_type='tab_switch',
            ).count(),
            1,
        )

    def test_invalid_event_type_rejected(self):
        response = self._log(
            'admin_delete'
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertEqual(
            ExamLog.objects.count(),
            0,
        )

    def test_ownership_enforced(self):
        self.client.logout()

        self.client.login(
            username='stuT',
            password='pass12345',
        )

        response = self._log(
            'tab_switch'
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_timestamp_is_server_generated(self):
        before = timezone.now()

        self._log('idle')

        after = timezone.now()

        log = ExamLog.objects.first()

        self.assertIsNotNone(
            log.timestamp
        )

        self.assertGreaterEqual(
            log.timestamp,
            before,
        )

        self.assertLessEqual(
            log.timestamp,
            after,
        )