from decimal import Decimal, InvalidOperation
import secrets
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
import string
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

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
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

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )

    questions = Question.objects.filter(
        Q(is_global=True) | Q(created_by=request.user),
        is_active=True,
    ).select_related(
        'subject',
        'topic',
    )

    # -------------------------
    # Filters
    # -------------------------

    source = request.GET.get('source', 'all').strip()
    subject_id = request.GET.get('subject', '').strip()
    topic_id = request.GET.get('topic', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    search = request.GET.get('search', '').strip()

    if source == 'global':
        questions = questions.filter(
            is_global=True
        )

    elif source == 'own':
        questions = questions.filter(
            created_by=request.user,
            is_global=False,
        )

    if subject_id:
        questions = questions.filter(
            subject_id=subject_id
        )

    if topic_id:
        questions = questions.filter(
            topic_id=topic_id
        )

    if difficulty:
        questions = questions.filter(
            difficulty_level=difficulty
        )

    if search:
        questions = questions.filter(
            Q(question_text__icontains=search)
            | Q(explanation__icontains=search)
        )

    questions = questions.order_by(
        'subject__name',
        'topic__name',
        'id',
    )

    subjects = Subject.objects.filter(
        is_active=True
    ).order_by('name')

    topics = Topic.objects.filter(
        is_active=True
    ).select_related(
        'subject'
    ).order_by(
        'subject__name',
        'name',
    )

    # -------------------------
    # Save selected questions
    # -------------------------

    if request.method == 'POST':

        selected_ids = request.POST.getlist(
            'questions'
        )

        if not selected_ids:
            messages.error(
                request,
                'Please select at least one question.'
            )

        else:

            # Only allow questions that this teacher
            # is actually allowed to use.
            allowed_questions = Question.objects.filter(
                Q(is_global=True) | Q(created_by=request.user),
                is_active=True,
                id__in=selected_ids,
            )

            allowed_map = {
                str(question.id): question
                for question in allowed_questions
            }

            if len(allowed_map) != len(set(selected_ids)):
                messages.error(
                    request,
                    'One or more selected questions are not available to you.'
                )

            else:

                selected_questions = []

                try:

                    for order, question_id in enumerate(
                        selected_ids,
                        start=1
                    ):

                        marks_value = request.POST.get(
                            f'marks_{question_id}',
                            ''
                        ).strip()

                        marks = Decimal(marks_value)

                        if marks <= 0:
                            raise ValueError

                        selected_questions.append(
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

                    with transaction.atomic():

                        ConductedExamQuestion.objects.filter(
                            exam=exam
                        ).delete()

                        ConductedExamQuestion.objects.bulk_create(
                            selected_questions
                        )

                    messages.success(
                        request,
                        'Questions saved successfully.'
                    )

                    return redirect(
                        'teacher_review_exam',
                        exam_id=exam.id,
                    )

    return render(
        request,
        'teachers/select_exam_questions.html',
        {
            'exam': exam,
            'questions': questions,
            'subjects': subjects,
            'topics': topics,
            'source': source,
            'selected_subject': subject_id,
            'selected_topic': topic_id,
            'selected_difficulty': difficulty,
            'search': search,
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

@role_required('teacher')
def exam_monitor_data(request, exam_id):

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
    )

    participants = exam.participants.select_related(
        'student'
    ).order_by('joined_at')

    return JsonResponse({
        'exam_status': exam.status,

        'participants': [
            {
                'id': participant.id,

                'username': participant.student.username,

                'first_name': participant.student.first_name,

                'last_name': participant.student.last_name,

                'joined_at': participant.joined_at.strftime(
                    '%d %b %Y, %I:%M %p'
                ),

                'status': participant.status,

                'score': participant.score,

                'total_marks': participant.total_marks,

                'violation_count': participant.violation_count,
            }

            for participant in participants
        ],
    })

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

    return render(
        request,
        'teachers/previous_exam_monitor.html',
        {
            'exam': exam,
            'participants': participants,
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
def previous_exam_pdf(request, exam_id):

    exam = get_object_or_404(
        ConductedExam,
        pk=exam_id,
        teacher=request.user,
        status='completed',
    )

    participants = exam.participants.select_related(
        'student'
    ).order_by('joined_at')


    # ---------------------------------------------------------
    # RESPONSE
    # ---------------------------------------------------------

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'attachment; '
        f'filename="exam_{exam.id}_report.pdf"'
    )


    # ---------------------------------------------------------
    # PDF DOCUMENT
    # ---------------------------------------------------------

    document = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )


    styles = getSampleStyleSheet()


    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    title_style = styles['Title']

    title_style.alignment = TA_CENTER


    elements = []


    elements.append(
        Paragraph(
            'PrepX - Exam Report',
            title_style
        )
    )


    elements.append(
        Spacer(
            1,
            15
        )
    )


    # ---------------------------------------------------------
    # EXAM DETAILS
    # ---------------------------------------------------------

    exam_details = [

        ['Exam Name', exam.exam_name],

        ['Exam Key', exam.exam_key or '-'],

        [
            'Started At',
            (
                exam.started_at.strftime(
                    '%d %b %Y, %I:%M %p'
                )
                if exam.started_at
                else '-'
            )
        ],

        [
            'Duration',
            f'{exam.duration_minutes} minutes'
        ],

        [
            'Questions',
            str(exam.exam_questions.count())
        ],

        [
            'Students',
            str(participants.count())
        ],

    ]


    exam_table = Table(
        exam_details,
        colWidths=[120, 300]
    )


    exam_table.setStyle(
        TableStyle([

            (
                'BACKGROUND',
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),

            (
                'FONTNAME',
                (0, 0),
                (0, -1),
                'Helvetica-Bold'
            ),

            (
                'GRID',
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                'VALIGN',
                (0, 0),
                (-1, -1),
                'MIDDLE'
            ),

            (
                'LEFTPADDING',
                (0, 0),
                (-1, -1),
                6
            ),

            (
                'RIGHTPADDING',
                (0, 0),
                (-1, -1),
                6
            ),

        ])
    )


    elements.append(
        exam_table
    )


    elements.append(
        Spacer(
            1,
            20
        )
    )


    # ---------------------------------------------------------
    # STUDENT RESULTS
    # ---------------------------------------------------------

    table_data = [

        [
            '#',
            'Student',
            'Joined At',
            'Submitted At',
            'Status',
            'Score',
            'Violations',
        ]

    ]


    for index, participant in enumerate(
        participants,
        start=1
    ):

        student_name = (
            participant.student.get_full_name()
            or participant.student.username
        )


        joined_at = (
            participant.joined_at.strftime(
                '%d %b %Y, %I:%M %p'
            )
            if participant.joined_at
            else '-'
        )


        submitted_at = (
            participant.submitted_at.strftime(
                '%d %b %Y, %I:%M %p'
            )
            if participant.submitted_at
            else '-'
        )


        status = (
            participant.get_status_display()
        )


        score = (
            f'{participant.score} / '
            f'{participant.total_marks}'
        )


        table_data.append([

            str(index),

            student_name,

            joined_at,

            submitted_at,

            status,

            score,

            str(
                participant.violation_count
            ),

        ])


    student_table = Table(
        table_data,
        repeatRows=1,
        colWidths=[
            30,
            130,
            120,
            120,
            100,
            80,
            70,
        ]
    )


    student_table.setStyle(
        TableStyle([

            (
                'BACKGROUND',
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                'TEXTCOLOR',
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                'FONTNAME',
                (0, 0),
                (-1, 0),
                'Helvetica-Bold'
            ),

            (
                'GRID',
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                'VALIGN',
                (0, 0),
                (-1, -1),
                'MIDDLE'
            ),

            (
                'LEFTPADDING',
                (0, 0),
                (-1, -1),
                5
            ),

            (
                'RIGHTPADDING',
                (0, 0),
                (-1, -1),
                5
            ),

        ])
    )


    elements.append(
        student_table
    )


    # ---------------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------------

    document.build(
        elements
    )


    return response

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