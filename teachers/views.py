from decimal import Decimal, InvalidOperation
from .reporting import build_exam_report, export_csv, export_excel
from results.services import (
    get_conducted_exam_leaderboard,
    get_conducted_exam_summary,
)
import secrets
import os
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
import string
from xml.sax.saxutils import escape
from accounts.decorators import role_required
from questions.models import Question
from subjects.models import Subject, Topic
from .forms import ConductedExamForm
from .models import ConductedExam, ConductedExamQuestion
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from .models import (
    ConductedExam,
    ConductedExamQuestion,
    ConductedExamParticipant,
)
from teachers.models import (
    ConductedExam,
    ConductedExamParticipant,
    ConductedExamAnswer,
)
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
)

@role_required('teacher')
def create_exam(request):

    form = ConductedExamForm(
        request.POST or None
    )

    if request.method == 'POST' and form.is_valid():

        exam = form.save(commit=False)
        exam.teacher = request.user
        exam.save()

        return redirect(
            'teacher_select_exam_questions',
            exam_id=exam.id,
        )

    return render(
        request,
        'teachers/create_exam.html',
        {'form': form}
    )

@role_required('teacher')
def select_exam_questions(request, exam_id):

    # =========================================================
    # GET EXAM
    # =========================================================

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )


    # =========================================================
    # SESSION KEY
    # =========================================================

    selection_session_key = (
        f'prepx_exam_{exam.id}_selected_questions'
    )


    # =========================================================
    # LOAD TEMPORARY SELECTION
    # =========================================================

    selected_questions = request.session.get(
        selection_session_key,
        {}
    )


    # Make sure session data is a dictionary.

    if not isinstance(
        selected_questions,
        dict
    ):

        selected_questions = {}


    # =========================================================
    # RESTORE DATABASE QUESTIONS
    # =========================================================
    #
    # If this exam already has questions saved in DB and
    # session does not have selection yet, restore them.
    #
    # =========================================================

    if not selected_questions:

        existing_questions = (
            ConductedExamQuestion.objects.filter(
                exam=exam
            ).order_by(
                'question_order'
            )
        )


        for exam_question in existing_questions:

            selected_questions[
                str(
                    exam_question.question_id
                )
            ] = str(
                exam_question.marks
            )


        if selected_questions:

            request.session[
                selection_session_key
            ] = selected_questions

            request.session.modified = True


    # =========================================================
    # FILTER VALUES
    # =========================================================

    source = request.GET.get(
        'source',
        'all'
    ).strip()


    subject_id = request.GET.get(
        'subject',
        ''
    ).strip()


    topic_id = request.GET.get(
        'topic',
        ''
    ).strip()


    difficulty = request.GET.get(
        'difficulty',
        ''
    ).strip()


    search = request.GET.get(
        'search',
        ''
    ).strip()


    # =========================================================
    # RESTORE SELECTION SENT BY FILTER FORM
    # =========================================================
    #
    # When Apply Filters is clicked, the currently selected
    # questions are sent through hidden GET fields.
    #
    # These are merged into the existing session selection.
    #
    # =========================================================

    carried_question_ids = request.GET.getlist(
        'selected_questions'
    )


    if carried_question_ids:

        for question_id in carried_question_ids:

            question_id = str(
                question_id
            )


            marks_value = request.GET.get(
                f'selected_marks_{question_id}',
                '1'
            ).strip()


            if not marks_value:

                marks_value = '1'


            selected_questions[
                question_id
            ] = marks_value


        request.session[
            selection_session_key
        ] = selected_questions

        request.session.modified = True


    # =========================================================
    # QUESTIONS QUERY
    # =========================================================

    questions = Question.objects.filter(
        Q(is_global=True)
        |
        Q(created_by=request.user),
        is_active=True,
    ).select_related(
        'subject',
        'topic',
    )


    # =========================================================
    # SOURCE FILTER
    # =========================================================

    if source == 'global':

        questions = questions.filter(
            is_global=True
        )


    elif source == 'own':

        questions = questions.filter(
            created_by=request.user,
            is_global=False,
        )


    # =========================================================
    # SUBJECT FILTER
    # =========================================================

    if subject_id:

        questions = questions.filter(
            subject_id=subject_id
        )


    # =========================================================
    # TOPIC FILTER
    # =========================================================

    if topic_id:

        questions = questions.filter(
            topic_id=topic_id
        )


    # =========================================================
    # DIFFICULTY FILTER
    # =========================================================

    if difficulty:

        questions = questions.filter(
            difficulty_level=difficulty
        )


    # =========================================================
    # SEARCH FILTER
    # =========================================================

    if search:

        questions = questions.filter(
            Q(
                question_text__icontains=search
            )
            |
            Q(
                explanation__icontains=search
            )
        )


    # =========================================================
    # ORDER QUESTIONS
    # =========================================================

    questions = questions.order_by(
        'subject__name',
        'topic__name',
        'id',
    )


    # =========================================================
    # MARK SELECTED QUESTIONS
    # =========================================================

    for question in questions:

        question_id = str(
            question.id
        )


        question.is_selected = (
            question_id in selected_questions
        )


        question.selected_marks = (
            selected_questions.get(
                question_id,
                '1'
            )
        )


    # =========================================================
    # SUBJECTS
    # =========================================================

    subjects = Subject.objects.filter(
        is_active=True
    ).order_by(
        'name'
    )


    # =========================================================
    # TOPICS
    # =========================================================

    topics = Topic.objects.filter(
        is_active=True
    ).select_related(
        'subject'
    ).order_by(
        'subject__name',
        'name',
    )


    # =========================================================
    # DIFFICULTY LEVELS
    # =========================================================

    difficulty_levels = range(
        1,
        11
    )


    # =========================================================
    # POST - CONTINUE
    # =========================================================

    if request.method == 'POST':

        selected_ids = request.POST.getlist(
            'questions'
        )


        # =====================================================
        # CURRENT FILTERED PAGE QUESTION IDS
        # =====================================================

        current_page_question_ids = {
            str(question.id)
            for question in questions
        }


        # =====================================================
        # REMOVE ONLY UNCHECKED QUESTIONS FROM
        # CURRENT FILTERED PAGE
        # =====================================================

        for question_id in current_page_question_ids:

            if question_id not in selected_ids:

                selected_questions.pop(
                    question_id,
                    None
                )


        # =====================================================
        # ADD / UPDATE CURRENT PAGE SELECTION
        # =====================================================

        for question_id in selected_ids:

            question_id = str(
                question_id
            )


            marks_value = request.POST.get(
                f'marks_{question_id}',
                '1'
            ).strip()


            if not marks_value:

                marks_value = '1'


            selected_questions[
                question_id
            ] = marks_value


        # =====================================================
        # SAVE SESSION
        # =====================================================

        request.session[
            selection_session_key
        ] = selected_questions

        request.session.modified = True


        # =====================================================
        # CHECK SELECTION
        # =====================================================

        if not selected_questions:

            messages.error(
                request,
                'Please select at least one question.'
            )


        else:

            final_selected_ids = list(
                selected_questions.keys()
            )


            # =================================================
            # VALIDATE QUESTION ACCESS
            # =================================================

            allowed_questions = Question.objects.filter(
                Q(is_global=True)
                |
                Q(created_by=request.user),
                is_active=True,
                id__in=final_selected_ids,
            )


            allowed_map = {
                str(question.id): question
                for question in allowed_questions
            }


            if (
                len(allowed_map)
                != len(final_selected_ids)
            ):

                messages.error(
                    request,
                    'One or more selected questions are not available to you.'
                )


            else:

                selected_exam_questions = []


                # =============================================
                # VALIDATE MARKS
                # =============================================

                try:

                    for order, question_id in enumerate(
                        final_selected_ids,
                        start=1
                    ):

                        marks_value = (
                            selected_questions.get(
                                question_id,
                                '1'
                            )
                        )


                        marks = Decimal(
                            marks_value
                        )


                        if marks <= 0:

                            raise ValueError


                        selected_exam_questions.append(
                            ConductedExamQuestion(
                                exam=exam,
                                question=allowed_map[
                                    question_id
                                ],
                                marks=marks,
                                question_order=order,
                            )
                        )


                except (
                    InvalidOperation,
                    ValueError,
                    TypeError,
                ):

                    messages.error(
                        request,
                        'Every selected question must have marks greater than 0.'
                    )


                else:

                    # =========================================
                    # SAVE TO DATABASE
                    # =========================================

                    with transaction.atomic():

                        ConductedExamQuestion.objects.filter(
                            exam=exam
                        ).delete()


                        ConductedExamQuestion.objects.bulk_create(
                            selected_exam_questions
                        )


                    # =================================================
                    # KEEP SESSION
                    # =================================================
                    #
                    # Required so Review -> Back can restore
                    # selected questions.
                    #
                    # =================================================

                    messages.success(
                        request,
                        'Questions saved successfully.'
                    )


                    return redirect(
                        'teacher_review_exam',
                        exam_id=exam.id,
                    )


    # =========================================================
    # FINAL SELECTED IDS
    # =========================================================

    selected_question_ids = list(
        selected_questions.keys()
    )


    # =========================================================
    # RENDER TEMPLATE
    # =========================================================

    return render(
        request,
        'teachers/select_exam_questions.html',
        {
            'exam': exam,

            'questions': questions,

            'subjects': subjects,

            'topics': topics,

            'difficulty_levels': difficulty_levels,

            'source': source,

            'selected_subject': subject_id,

            'selected_topic': topic_id,

            'selected_difficulty': difficulty,

            'search': search,

            'selected_questions': selected_questions,

            'selected_question_ids': (
                selected_question_ids
            ),

            'selected_question_count': (
                len(selected_question_ids)
            ),
        }
    )

@role_required('teacher')
def review_exam(request, exam_id):

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )

    selected_questions = (
        ConductedExamQuestion.objects
        .filter(exam=exam)
        .select_related(
            'question',
            'question__subject',
            'question__topic',
        )
        .order_by('question_order')
    )

    total_questions = selected_questions.count()

    total_marks = sum(
        item.marks
        for item in selected_questions
    )

    return render(
        request,
        'teachers/review_exam.html',
        {
            'exam': exam,
            'selected_questions': selected_questions,
            'total_questions': total_questions,
            'total_marks': total_marks,
        }
    )

@role_required('teacher')
def launch_exam(request, exam_id):

    if request.method != 'POST':
        return redirect(
            'teacher_review_exam',
            exam_id=exam_id,
        )

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )

    # Exam must still be in draft state.
    if exam.status != 'draft':

        messages.error(
            request,
            'This exam cannot be launched.'
        )

        return redirect(
            'teacher_review_exam',
            exam_id=exam.id,
        )

    # At least one question is required.
    if not ConductedExamQuestion.objects.filter(
        exam=exam
    ).exists():

        messages.error(
            request,
            'You must select at least one question.'
        )

        return redirect(
            'teacher_review_exam',
            exam_id=exam.id,
        )

    # Generate a unique 6-character exam key.
    alphabet = string.ascii_uppercase + string.digits

    while True:

        exam_key = ''.join(
            secrets.choice(alphabet)
            for _ in range(6)
        )

        if not ConductedExam.objects.filter(
            exam_key=exam_key
        ).exists():

            break

    with transaction.atomic():

        exam.exam_key = exam_key
        exam.status = 'waiting'

        exam.save(
            update_fields=[
                'exam_key',
                'status',
                'updated_at',
            ]
        )

    messages.success(
        request,
        'Exam launched successfully.'
    )

    return redirect(
        'teacher_exam_monitor',
        exam_id=exam.id,
    )

@role_required('teacher')
def exam_monitor(request, exam_id):

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )

    participants = exam.participants.select_related(
        'student'
    ).order_by('joined_at')

    return render(
        request,
        'teachers/exam_monitor.html',
        {
            'exam': exam,
            'participants': participants,
        }
    )

from django.utils import timezone


@role_required('teacher')
def exam_monitor_data(request, exam_id):

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )

    participants = (
        exam.participants
        .select_related('student')
        .order_by('joined_at')
    )

    return JsonResponse(
        {
            'exam_status': exam.status,

            'participants': [

                {
                    'id': participant.id,

                    'username': participant.student.username,

                    'first_name': participant.student.first_name,

                    'last_name': participant.student.last_name,

                    # =========================================
                    # CONVERT UTC → ASIA/KOLKATA
                    # =========================================

                    'joined_at': (
                        timezone.localtime(
                            participant.joined_at
                        ).strftime(
                            '%d %b %Y, %I:%M %p'
                        )
                    ),

                    'status': participant.status,

                    'score': participant.score,

                    'total_marks': participant.total_marks,

                    'violation_count': (
                        participant.violation_count
                    ),
                }

                for participant in participants
            ],
        }
    )

@role_required('teacher')
def previous_exam_monitor(request, exam_id):

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
        status='completed',
    )

    participants = exam.participants.select_related(
        'student'
    ).prefetch_related(
        'security_logs'
    ).order_by('joined_at')
    leaderboard = get_conducted_exam_leaderboard(exam)
    summary = get_conducted_exam_summary(leaderboard)

    return render(
        request,
        'teachers/previous_exam_monitor.html',
        {
            'exam': exam,
            'participants': participants,
            'leaderboard': leaderboard,
            'summary': summary,
        }
    )

@role_required('teacher')
def start_exam(request, exam_id):

    if request.method != 'POST':
        return redirect(
            'teacher_exam_monitor',
            exam_id=exam_id,
        )

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )

    # Exam must be waiting for students.
    if exam.status != 'waiting':

        messages.error(
            request,
            'This exam cannot be started.'
        )

        return redirect(
            'teacher_exam_monitor',
            exam_id=exam.id,
        )

    participants = ConductedExamParticipant.objects.filter(
        exam=exam,
        status='joined',
    )

    if not participants.exists():

        messages.error(
            request,
            'At least one student must join before starting the exam.'
        )

        return redirect(
            'teacher_exam_monitor',
            exam_id=exam.id,
        )

    started_at = timezone.now()

    ends_at = started_at + timedelta(
        minutes=exam.duration_minutes
    )

    with transaction.atomic():

        exam.status = 'ongoing'
        exam.started_at = started_at
        exam.ends_at = ends_at

        exam.save(
            update_fields=[
                'status',
                'started_at',
                'ends_at',
                'updated_at',
            ]
        )

        participants.update(
            status='ongoing',
            started_at=started_at,
            updated_at=started_at,
        )

    messages.success(
        request,
        'Exam has started successfully.'
    )

    return redirect(
        'teacher_exam_monitor',
        exam_id=exam.id,
    )

@role_required('teacher')
def end_exam(request, exam_id):

    if request.method != 'POST':
        return redirect(
            'teacher_exam_monitor',
            exam_id=exam_id,
        )

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )

    # ---------------------------------------------------------
    # EXAM MUST BE ONGOING
    # ---------------------------------------------------------

    if exam.status != 'ongoing':

        messages.error(
            request,
            'This exam is not currently ongoing.'
        )

        return redirect(
            'teacher_exam_monitor',
            exam_id=exam.id,
        )

    now = timezone.now()

    # ---------------------------------------------------------
    # GET ONGOING PARTICIPANTS
    # ---------------------------------------------------------

    participants = ConductedExamParticipant.objects.filter(
        exam=exam,
        status='ongoing',
    )

    # ---------------------------------------------------------
    # SUBMIT ONGOING STUDENTS
    # ---------------------------------------------------------

    for participant in participants:

        exam_questions = exam.exam_questions.select_related(
            'question'
        ).order_by('question_order')

        total_score = 0
        total_marks = 0

        for exam_question in exam_questions:

            total_marks += exam_question.marks

            answer = ConductedExamAnswer.objects.filter(
                participant=participant,
                exam_question=exam_question,
            ).first()

            if answer is None:
                continue

            selected_option = answer.selected_option

            if not selected_option:

                answer.is_correct = None
                answer.marks_obtained = 0

                answer.save(
                    update_fields=[
                        'is_correct',
                        'marks_obtained',
                        'updated_at',
                    ]
                )

                continue

            correct_option = (
                exam_question.question.correct_option
            )

            # -------------------------------------------------
            # CORRECT ANSWER
            # -------------------------------------------------

            if selected_option == correct_option:

                answer.is_correct = True

                answer.marks_obtained = (
                    exam_question.marks
                )

                total_score += (
                    exam_question.marks
                )

            # -------------------------------------------------
            # WRONG ANSWER
            # -------------------------------------------------

            else:

                answer.is_correct = False

                if exam.negative_marking_enabled:

                    answer.marks_obtained = (
                        -exam.negative_marks
                    )

                    total_score -= (
                        exam.negative_marks
                    )

                else:

                    answer.marks_obtained = 0

            answer.save(
                update_fields=[
                    'is_correct',
                    'marks_obtained',
                    'updated_at',
                ]
            )

        # -----------------------------------------------------
        # MARK PARTICIPANT AS AUTO SUBMITTED
        # -----------------------------------------------------

        participant.score = total_score

        participant.total_marks = total_marks

        participant.status = 'auto_submitted'

        participant.submitted_at = now

        participant.save(
            update_fields=[
                'score',
                'total_marks',
                'status',
                'submitted_at',
                'updated_at',
            ]
        )

        from results.services import get_or_create_conducted_result

        get_or_create_conducted_result(
            participant
        )

    # ---------------------------------------------------------
    # COMPLETE EXAM
    # ---------------------------------------------------------

    exam.status = 'completed'

    exam.save(
        update_fields=[
            'status',
            'updated_at',
        ]
    )

    messages.success(
        request,
        'Exam has been completed successfully.'
    )

    return redirect(
        'teacher_exam_monitor',
        exam_id=exam.id,
    )

@role_required('student')
def exam_timer_status(request, exam_id):

    participant = ConductedExamParticipant.objects.filter(
        exam_id=exam_id,
        student=request.user,
        status='ongoing',
    ).select_related('exam').first()

    if participant is None:

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam is not active.'
            },
            status=403
        )


    exam = participant.exam


    # ---------------------------------------------------------
    # EXAM MUST BE ONGOING
    # ---------------------------------------------------------

    if exam.status != 'ongoing':

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam is not ongoing.'
            },
            status=400
        )


    # ---------------------------------------------------------
    # EXAM END TIME MUST EXIST
    # ---------------------------------------------------------

    if exam.ends_at is None:

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam end time is not available.'
            },
            status=400
        )


    # ---------------------------------------------------------
    # CALCULATE REMAINING TIME
    # ---------------------------------------------------------

    now = timezone.now()

    remaining_seconds = int(
        (exam.ends_at - now).total_seconds()
    )


    # ---------------------------------------------------------
    # EXAM TIME EXPIRED
    # ---------------------------------------------------------

    if remaining_seconds <= 0:

        return JsonResponse(
            {
                'success': True,
                'expired': True,
                'remaining_seconds': 0,
            }
        )


    # ---------------------------------------------------------
    # TIME STILL REMAINING
    # ---------------------------------------------------------

    return JsonResponse(
        {
            'success': True,
            'expired': False,
            'remaining_seconds': remaining_seconds,
        }
    )

@role_required('teacher')
def previous_conducted_exams(request):

    exams = ConductedExam.objects.filter(
        teacher=request.user,
        status='completed',
    ).prefetch_related(
        'participants',
        'exam_questions',
    ).order_by('-updated_at')

    return render(
        request,
        'teachers/previous_conducted_exams.html',
        {
            'exams': exams,
        }
    )

@role_required('teacher')
def ongoing_exams(request):

    exams = ConductedExam.objects.filter(
        teacher=request.user,
        status='ongoing',
    ).order_by('-started_at')

    return render(
        request,
        'teachers/ongoing_exams.html',
        {
            'exams': exams,
        }
    )

@role_required('teacher')
def previous_exam_pdf(request, exam_id):
    """Download the owning teacher's completed examination report."""
    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
        status='completed',
    )

    report = build_exam_report(exam)
    leaderboard = report['leaderboard']
    summary = report['summary']
    participants = report['participants']
    total_students = report['total_students']
    total_questions = report['total_questions']
    total_possible_marks = report['total_possible_marks']
    correct_counts = report['correct_counts']

    # =========================================================
    # BRAND COLORS / PDF RESPONSE
    # =========================================================
    BRAND_DARK = colors.HexColor('#3B2418')
    BRAND_GOLD = colors.HexColor('#F4B400')
    BRAND_LIGHT_GOLD = colors.HexColor('#FFF6D8')
    TEXT_DARK = colors.HexColor('#292524')
    TEXT_MUTED = colors.HexColor('#78716C')
    BORDER = colors.HexColor('#E7E5E4')
    LIGHT_BG = colors.HexColor('#FAFAF9')
    DANGER = colors.HexColor('#B91C1C')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="PrepX_Exam_Report_{exam.id}.pdf"'
    )

    document = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title=f'PrepX - {exam.exam_name} Report',
        author='PrepX',
    )
    page_width, page_height = landscape(A4)
    content_width = page_width - 30 * mm

    # =========================================================
    # STYLES
    # =========================================================
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=2,
    )
    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#E7E5E4'),
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=TEXT_DARK,
        spaceAfter=8,
    )
    normal_style = ParagraphStyle(
        'NormalCustom',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=TEXT_DARK,
        wordWrap='CJK',
    )
    small_style = ParagraphStyle(
        'Small',
        parent=normal_style,
        fontSize=7,
        leading=9,
        textColor=TEXT_MUTED,
    )
    card_label_style = ParagraphStyle(
        'CardLabel',
        parent=styles['Normal'],
        fontSize=7,
        leading=9,
        textColor=TEXT_MUTED,
    )
    card_value_style = ParagraphStyle(
        'CardValue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=19,
        textColor=TEXT_DARK,
    )
    date_value_style = ParagraphStyle(
        'DateValue',
        parent=card_value_style,
        fontSize=11,
        leading=14,
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.white,
        alignment=TA_CENTER,
    )

    def paragraph(value, style=normal_style):
        return Paragraph(escape(str(value)), style)

    def card(label, value, value_style=card_value_style):
        return [
            paragraph(label, card_label_style),
            Spacer(1, 2),
            paragraph(value, value_style),
        ]

    def card_table(items, background, border, height):
        table = Table(
            [items],
            colWidths=[content_width / len(items)] * len(items),
            rowHeights=[height],
        )
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), background),
            ('BOX', (0, 0), (-1, -1), 0.6, border),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border),
            ('LEFTPADDING', (0, 0), (-1, -1), 5 * mm),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5 * mm),
            ('TOPPADDING', (0, 0), (-1, -1), 3 * mm),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3 * mm),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return table

    def display_date(value):
        if value is None:
            return '-'
        return timezone.localtime(value).strftime('%d %b %Y, %I:%M %p')

    # =========================================================
    # PAGE FOOTER
    # =========================================================
    def draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(
            15 * mm, 10 * mm,
            page_width - 15 * mm, 10 * mm,
        )
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(TEXT_MUTED)
        canvas.drawString(
            15 * mm, 6 * mm,
            'PrepX - Conducted Examination Report',
        )
        canvas.drawRightString(
            page_width - 15 * mm, 6 * mm,
            f'Page {doc.page}',
        )
        canvas.restoreState()

    elements = []

    # =========================================================
    # HEADER
    # =========================================================
    logo_path = os.path.join(
        settings.BASE_DIR, 'static', 'images', 'prepx-logo.png',
    )
    header_content = []

    if os.path.exists(logo_path):
        header_content.extend([
            Image(
                logo_path,
                width=35 * mm,
                height=8 * mm,
                kind='proportional',
            ),
            Spacer(1, 1 * mm),
        ])

    header_content.extend([
        Paragraph('CONDUCTED EXAMINATION REPORT', title_style),
        paragraph(exam.exam_name, subtitle_style),
    ])

    header_table = Table(
        [[header_content]],
        colWidths=[content_width],
        # Let the header grow if the logo or exam title needs more space.
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BRAND_DARK),
        ('LEFTPADDING', (0, 0), (-1, -1), 10 * mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10 * mm),
        ('TOPPADDING', (0, 0), (-1, -1), 4 * mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4 * mm),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.extend([header_table, Spacer(1, 6 * mm)])

    # =========================================================
    # EXAM INFORMATION
    # =========================================================
    completed_date = display_date(exam.ends_at)
    joined_students = exam.participants.count()

    info_cards = [
        card('EXAM DATE', completed_date, date_value_style),
        card('DURATION', f'{exam.duration_minutes} minutes'),
        card('QUESTIONS', total_questions),
        card('STUDENTS JOINED', joined_students),
    ]
    elements.extend([
        card_table(info_cards, LIGHT_BG, BORDER, 20 * mm),
        Spacer(1, 4 * mm),
        Paragraph('Performance Summary', section_style),
    ])

    # Summary uses evaluated students only, including negative scores.
    summary_cards = [
        card('EVALUATED STUDENTS', total_students),
        card('AVERAGE SCORE', f"{summary['average_score']:.2f}"),
        card('HIGHEST SCORE', f"{summary['highest_score']:.2f}"),
        card('TOTAL MARKS', f'{total_possible_marks:.2f}'),
    ]
    elements.extend([
        card_table(
            summary_cards, BRAND_LIGHT_GOLD, BRAND_GOLD, 20 * mm,
        ),
        Spacer(1, 5 * mm),
        Paragraph('Student Results', section_style),
    ])

    # =========================================================
    # STUDENT RESULTS TABLE
    # =========================================================
    headers = [
        'RANK', 'STUDENT', 'JOINED AT', 'SUBMITTED AT',
        'STATUS', 'SCORE', 'ACCURACY', 'TIME TAKEN', 'VIOLATIONS',
    ]
    table_data = [
        [paragraph(header, table_header_style) for header in headers]
    ]
    violation_rows = []

    for row_index, item in enumerate(leaderboard, start=1):
        participant = item['participant']
        student = participant.student
        student_name = student.get_full_name() or student.username

        correct = correct_counts.get(participant.pk, 0)
        accuracy = (
            f'{correct / total_questions * 100:.2f}%'
            if total_questions
            else 'N/A'
        )

        score = participant.score or Decimal('0')
        marks = participant.total_marks or Decimal('0')
        student_paragraph = Paragraph(
            f'<b>{escape(student_name)}</b><br/>'
            f'<font color="#78716C" size="7">'
            f'@{escape(student.username)}</font>',
            normal_style,
        )

        if participant.status == 'submitted':
            status_text = 'Submitted'
            status_color = '#15803D'
        else:
            status_text = 'Auto Submitted'
            status_color = '#B91C1C'

        status_paragraph = Paragraph(
            f'<font color="{status_color}">'
            f'<b>{status_text}</b></font>',
            normal_style,
        )
        score_paragraph = Paragraph(
            f'<b>{score:.2f}</b><br/>'
            f'<font color="#78716C">/ {marks:.2f}</font>',
            normal_style,
        )

        violation_count = participant.violation_count or 0
        violation_color = (
            '#B91C1C' if violation_count else '#15803D'
        )
        violation_paragraph = Paragraph(
            f'<font color="{violation_color}">'
            f'<b>{violation_count}</b></font>',
            normal_style,
        )
        if violation_count:
            violation_rows.append(row_index)

        table_data.append([
            paragraph(item['rank']),
            student_paragraph,
            paragraph(display_date(participant.joined_at), small_style),
            paragraph(display_date(participant.submitted_at), small_style),
            status_paragraph,
            score_paragraph,
            paragraph(accuracy),
            paragraph(item['time_taken'], small_style),
            violation_paragraph,
        ])

    if not leaderboard:
        table_data.append([
            paragraph('No finalized results are available.', small_style),
            '', '', '', '', '', '', '', '',
        ])

    # Landscape A4: 297 - 30 mm margins = 267 mm of available width.
    # All nine columns fit within that width.
    student_table = Table(
        table_data,
        repeatRows=1,
        colWidths=[
            12 * mm, 49 * mm, 34 * mm, 34 * mm, 31 * mm,
            28 * mm, 24 * mm, 34 * mm, 21 * mm,
        ],
        hAlign='LEFT',
    )
    student_table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('BOX', (0, 0), (-1, -1), 0.7, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 2 * mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2 * mm),
        ('TOPPADDING', (0, 0), (-1, -1), 3 * mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3 * mm),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (5, 1), (8, -1), 'CENTER'),
    ]
    if not leaderboard:
        student_table_style.append(('SPAN', (0, 1), (-1, 1)))

    for row_index in violation_rows:
        student_table_style.append(
            ('LINEBEFORE', (8, row_index), (8, row_index), 2, DANGER)
        )

    student_table.setStyle(TableStyle(student_table_style))
    elements.append(student_table)

    # =========================================================
    # REPORT NOTE
    # =========================================================
    elements.append(Spacer(1, 4 * mm))
    note = (
        'Ranks are ordered by higher score, then shorter exact '
        'completion time. Only finalized submissions with valid '
        'start and submission times are ranked. '
        'Accuracy is correct answers divided by total exam questions. '
        'Scores include the configured negative marking. '
        'Violation counts are based on recorded exam security events.'
    )
    report_note = Table(
        [[Paragraph(
            '<b>PrepX Security &amp; Evaluation</b><br/>'
            f'<font color="#78716C">{escape(note)}</font>',
            normal_style,
        )]],
        colWidths=[content_width],
    )
    report_note.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 5 * mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5 * mm),
        ('TOPPADDING', (0, 0), (-1, -1), 4 * mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4 * mm),
    ]))
    elements.append(report_note)

    document.build(
        elements,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer,
    )
    return response


def _download_exam_report(request, exam_id, file_format):
    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
        status='completed',
    )
    report = build_exam_report(exam)

    if file_format == 'csv':
        content = export_csv(report)
        content_type = 'text/csv; charset=utf-8'
    elif file_format == 'xlsx':
        content = export_excel(report)
        content_type = (
            'application/vnd.openxmlformats-officedocument.'
            'spreadsheetml.sheet'
        )
    else:
        raise ValueError('Unsupported report format.')

    response = HttpResponse(content, content_type=content_type)
    response['Content-Disposition'] = (
        f'attachment; filename="PrepX_Exam_Report_{exam.id}.{file_format}"'
    )
    return response


@role_required('teacher')
def previous_exam_csv(request, exam_id):
    return _download_exam_report(request, exam_id, 'csv')


@role_required('teacher')
def previous_exam_excel(request, exam_id):
    return _download_exam_report(request, exam_id, 'xlsx')
