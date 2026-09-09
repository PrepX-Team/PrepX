"""Focused Phase 5 reporting regression tests."""

import csv
from decimal import Decimal
from io import BytesIO, StringIO
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from questions.models import Question
from subjects.models import Subject, Topic
from .models import (
    ConductedExam, ConductedExamAnswer,
    ConductedExamParticipant, ConductedExamQuestion,
)
from .reporting import build_exam_report, export_csv, export_excel


class TeacherReportingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = User.objects.create_user(
            username='report_teacher', password='pass12345',
            role='teacher', is_approved=True,
        )
        cls.other_teacher = User.objects.create_user(
            username='report_other_teacher', password='pass12345',
            role='teacher', is_approved=True,
        )
        cls.student = User.objects.create_user(
            username='report_student', password='pass12345',
            role='student', is_approved=True,
        )
        cls.other_student = User.objects.create_user(
            username='report_other_student', password='pass12345',
            role='student', is_approved=True,
        )
        cls.unfinished_student = User.objects.create_user(
            username='report_unfinished', password='pass12345',
            role='student', is_approved=True,
        )
        subject = Subject.objects.create(name='Reporting Subject')
        topic = Topic.objects.create(subject=subject, name='Reporting Topic')
        cls.exam = ConductedExam.objects.create(
            teacher=cls.teacher, exam_name='Reporting Exam',
            duration_minutes=30, status='completed',
            negative_marking_enabled=True, negative_marks=Decimal('1'),
        )
        cls.exam_questions = []
        for index, marks in enumerate((2, 3), start=1):
            question = Question.objects.create(
                subject=subject, topic=topic,
                question_text=f'Report Question {index}',
                option_a='A', option_b='B', option_c='C', option_d='D',
                correct_option='A', explanation='Explanation.',
                difficulty_level=1, created_by=cls.teacher,
                is_global=True, status='approved',
            )
            cls.exam_questions.append(ConductedExamQuestion.objects.create(
                exam=cls.exam, question=question,
                marks=marks, question_order=index,
            ))

        start = timezone.now()
        cls.first = ConductedExamParticipant.objects.create(
            exam=cls.exam, student=cls.student, status='submitted',
            started_at=start,
            submitted_at=start + timezone.timedelta(minutes=10),
            score=Decimal('1'), total_marks=Decimal('5'),
        )
        cls.second = ConductedExamParticipant.objects.create(
            exam=cls.exam, student=cls.other_student, status='auto_submitted',
            started_at=start,
            submitted_at=start + timezone.timedelta(minutes=5),
            score=Decimal('-1'), total_marks=Decimal('5'),
        )
        ConductedExamParticipant.objects.create(
            exam=cls.exam, student=cls.unfinished_student,
            status='ongoing', started_at=start, score=100,
        )
        for participant, choices in (
            (cls.first, ('A', 'B')),
            (cls.second, ('B', None)),
        ):
            for exam_question, choice in zip(cls.exam_questions, choices):
                ConductedExamAnswer.objects.create(
                    participant=participant, exam_question=exam_question,
                    selected_option=choice,
                    is_correct=(
                        choice == 'A' if choice is not None else None
                    ),
                )

    def setUp(self):
        self.client.force_login(self.teacher)

    def test_report_uses_finalized_ranks_and_actual_accuracy(self):
        report = build_exam_report(self.exam)
        self.assertEqual(report['total_students'], 2)
        self.assertEqual([row['rank'] for row in report['rows']], [1, 2])
        self.assertEqual(report['rows'][0]['accuracy'], Decimal('50.00'))
        self.assertEqual(report['rows'][1]['accuracy'], Decimal('0.00'))
        self.assertEqual(report['rows'][0]['time_taken'], '10 min 00 sec')
        self.assertEqual(report['summary']['average_score'], Decimal('0.00'))
        self.assertEqual(report['summary']['highest_score'], Decimal('1'))
        self.assertEqual(report['summary']['lowest_score'], Decimal('-1'))
        self.assertEqual(report['total_possible_marks'], Decimal('5'))
        self.assertNotIn(
            'report_unfinished',
            [row['username'] for row in report['rows']],
        )

    def test_csv_contains_correct_fields_and_order(self):
        response = self.client.get(
            reverse('teacher_previous_exam_csv', args=[self.exam.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content[:3], b'\xef\xbb\xbf')
        rows = list(csv.reader(StringIO(response.content.decode('utf-8-sig'))))
        self.assertEqual(rows[1][0], '1')
        self.assertEqual(rows[1][8], '50.00')
        self.assertEqual(rows[2][6], '-1.00')
        self.assertEqual(len(rows), 3)

    def test_excel_has_real_numeric_cells(self):
        from openpyxl import load_workbook
        response = self.client.get(
            reverse('teacher_previous_exam_excel', args=[self.exam.pk])
        )
        self.assertEqual(response.status_code, 200)
        workbook = load_workbook(BytesIO(response.content), read_only=True)
        sheet = workbook['Student Results']
        self.assertEqual(sheet['A2'].value, 1)
        self.assertEqual(sheet['I2'].value, 50)
        self.assertEqual(sheet['G3'].value, -1)
        workbook.close()

    def test_pdf_is_generated_for_completed_exam(self):
        response = self.client.get(
            reverse('teacher_previous_exam_pdf', args=[self.exam.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_other_teacher_cannot_download_reports(self):
        self.client.force_login(self.other_teacher)
        for name in (
            'teacher_previous_exam_pdf',
            'teacher_previous_exam_csv',
            'teacher_previous_exam_excel',
        ):
            response = self.client.get(reverse(name, args=[self.exam.pk]))
            self.assertEqual(response.status_code, 404)

    def test_student_cannot_download_teacher_reports(self):
        self.client.force_login(self.student)
        for name in (
            'teacher_previous_exam_pdf',
            'teacher_previous_exam_csv',
            'teacher_previous_exam_excel',
        ):
            response = self.client.get(reverse(name, args=[self.exam.pk]))
            self.assertNotEqual(response.status_code, 200)

    def test_incomplete_exam_cannot_be_exported(self):
        self.exam.status = 'ongoing'
        self.exam.save(update_fields=['status'])
        for name in (
            'teacher_previous_exam_pdf',
            'teacher_previous_exam_csv',
            'teacher_previous_exam_excel',
        ):
            response = self.client.get(reverse(name, args=[self.exam.pk]))
            self.assertEqual(response.status_code, 404)

    def test_empty_report_has_headers_and_no_division_error(self):
        empty = ConductedExam.objects.create(
            teacher=self.teacher, exam_name='Empty Report',
            duration_minutes=10, status='completed',
        )
        report = build_exam_report(empty)
        self.assertEqual(report['total_students'], 0)
        self.assertEqual(report['rows'], [])
        self.assertEqual(report['summary']['average_score'], 0)
        self.assertEqual(len(list(csv.reader(StringIO(
            export_csv(report).decode('utf-8-sig')
        )))), 1)
        self.assertTrue(export_excel(report).startswith(b'PK'))
        response = self.client.get(
            reverse('teacher_previous_exam_pdf', args=[empty.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_csv_formula_injection_is_escaped(self):
        self.student.first_name = '=HYPERLINK("https://example.com")'
        self.student.last_name = ''
        self.student.save(update_fields=['first_name', 'last_name'])
        rows = list(csv.reader(StringIO(
            export_csv(build_exam_report(self.exam)).decode('utf-8-sig')
        )))
        self.assertTrue(rows[1][1].startswith("'=HYPERLINK"))
