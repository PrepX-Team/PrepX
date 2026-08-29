from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from accounts.decorators import role_required

from teachers.models import (
    ConductedExam,
    ConductedExamParticipant,
    ConductedExamAnswer,
)


@role_required('student')
def join_exam(request):

    if request.method == 'POST':

        exam_key = request.POST.get(
            'exam_key',
            ''
        ).strip().upper()

        if not exam_key:
            messages.error(
                request,
                'Please enter an exam key.'
            )

            return render(
                request,
                'students/join_exam.html'
            )

        # Find a waiting exam using the exam key.
        exam = ConductedExam.objects.filter(
            exam_key=exam_key,
            status='waiting',
            is_active=True,
        ).first()

        if exam is None:
            messages.error(
                request,
                'Invalid exam key or this exam is not available.'
            )

            return render(
                request,
                'students/join_exam.html'
            )

        # Prevent the same student from joining twice.
        already_joined = ConductedExamParticipant.objects.filter(
            exam=exam,
            student=request.user,
        ).exists()

        if already_joined:
            return redirect(
                'student_exam_waiting',
                exam_id=exam.id,
            )

        try:

            ConductedExamParticipant.objects.create(
                exam=exam,
                student=request.user,
            )

        except IntegrityError:

            return redirect(
                'student_exam_waiting',
                exam_id=exam.id,
            )

        return redirect(
            'student_exam_waiting',
            exam_id=exam.id,
        )

    return render(
        request,
        'students/join_exam.html'
    )


@role_required('student')
def exam_waiting(request, exam_id):

    participant = ConductedExamParticipant.objects.filter(
        exam_id=exam_id,
        student=request.user,
    ).select_related('exam').first()

    if participant is None:

        messages.error(
            request,
            'You have not joined this exam.'
        )

        return redirect('student_join_exam')

    return render(
        request,
        'students/exam_waiting.html',
        {
            'participant': participant,
            'exam': participant.exam,
        }
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

    if exam.status != 'ongoing':

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam is not ongoing.'
            },
            status=400
        )

    if exam.ends_at is None:

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam end time is not available.'
            },
            status=400
        )

    now = timezone.now()

    remaining_seconds = int(
        (exam.ends_at - now).total_seconds()
    )

    if remaining_seconds <= 0:

        return JsonResponse(
            {
                'success': True,
                'expired': True,
                'remaining_seconds': 0,
            }
        )

    return JsonResponse(
        {
            'success': True,
            'expired': False,
            'remaining_seconds': remaining_seconds,
        }
    )

@role_required('student')
@require_POST
def auto_submit_exam(request, exam_id):

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

    if exam.ends_at is None:

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam end time is not available.'
            },
            status=400
        )

    # ---------------------------------------------------------
    # SERVER-SIDE EXPIRY CHECK
    # ---------------------------------------------------------

    if timezone.now() < exam.ends_at:

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam time has not expired yet.'
            },
            status=400
        )

    # ---------------------------------------------------------
    # GET QUESTIONS
    # ---------------------------------------------------------

    exam_questions = exam.exam_questions.select_related(
        'question'
    ).order_by('question_order')

    total_score = 0
    total_marks = 0

    # ---------------------------------------------------------
    # CALCULATE RESULT FROM SAVED ANSWERS
    # ---------------------------------------------------------

    for exam_question in exam_questions:

        total_marks += exam_question.marks

        answer = ConductedExamAnswer.objects.filter(
            participant=participant,
            exam_question=exam_question,
        ).first()

        # Student did not answer this question.
        if answer is None:
            continue

        selected_option = answer.selected_option

        # No selected option.
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

        # -----------------------------------------------------
        # CORRECT
        # -----------------------------------------------------

        if selected_option == correct_option:

            answer.is_correct = True

            answer.marks_obtained = (
                exam_question.marks
            )

            total_score += (
                exam_question.marks
            )

        # -----------------------------------------------------
        # INCORRECT
        # -----------------------------------------------------

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

    # ---------------------------------------------------------
    # UPDATE PARTICIPANT
    # ---------------------------------------------------------

    participant.score = total_score

    participant.total_marks = total_marks

    participant.status = 'auto_submitted'

    participant.submitted_at = timezone.now()

    participant.save(
        update_fields=[
            'score',
            'total_marks',
            'status',
            'submitted_at',
            'updated_at',
        ]
    )

    return JsonResponse(
        {
            'success': True,
            'redirect_url': (
                f'/students/exams/'
                f'{exam.id}/submitted/'
            ),
        }
    )

@role_required('student')
def take_exam(request, exam_id):

    participant = ConductedExamParticipant.objects.filter(
        exam_id=exam_id,
        student=request.user,
        status='ongoing',
    ).select_related('exam').first()

    if participant is None:

        messages.error(
            request,
            'You cannot access this exam.'
        )

        return redirect('student_join_exam')

    exam = participant.exam

    exam_questions = exam.exam_questions.select_related(
        'question'
    ).order_by('question_order')

    if not exam_questions.exists():

        messages.error(
            request,
            'This exam has no questions.'
        )

        return redirect(
            'student_exam_waiting',
            exam_id=exam.id,
        )


    # =========================================================
    # RESTORE SAVED ANSWERS
    # =========================================================

    for exam_question in exam_questions:

        answer = participant.answers.filter(
            exam_question=exam_question
        ).first()

        exam_question.saved_option = (
            answer.selected_option
            if answer
            else ''
        )


    # =========================================================
    # SUBMIT EXAM
    # =========================================================

    if request.method == 'POST':

        total_score = 0
        total_marks = 0

        for exam_question in exam_questions:

            total_marks += exam_question.marks

            selected_option = request.POST.get(
                f'question_{exam_question.id}'
            )

            # Get or create answer record
            answer, created = ConductedExamAnswer.objects.get_or_create(
                participant=participant,
                exam_question=exam_question,
            )

            answer.selected_option = selected_option


            # -------------------------------------------------
            # NO ANSWER
            # -------------------------------------------------

            if not selected_option:

                answer.is_correct = None

                answer.marks_obtained = 0

                answer.answered_at = None


            # -------------------------------------------------
            # ANSWER PROVIDED
            # -------------------------------------------------

            else:

                answer.answered_at = timezone.now()

                correct_option = (
                    exam_question.question.correct_option
                )


                # ---------------------------------------------
                # CORRECT
                # ---------------------------------------------

                if selected_option == correct_option:

                    answer.is_correct = True

                    answer.marks_obtained = (
                        exam_question.marks
                    )

                    total_score += (
                        exam_question.marks
                    )


                # ---------------------------------------------
                # INCORRECT
                # ---------------------------------------------

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


            answer.save()


        # =====================================================
        # UPDATE PARTICIPANT
        # =====================================================

        participant.score = total_score

        participant.total_marks = total_marks

        participant.status = 'submitted'

        participant.submitted_at = timezone.now()

        participant.save(
            update_fields=[
                'score',
                'total_marks',
                'status',
                'submitted_at',
                'updated_at',
            ]
        )


        messages.success(
            request,
            'Your exam has been submitted successfully.'
        )


        return redirect(
            'student_exam_submitted',
            exam_id=exam.id,
        )


    # =========================================================
    # DISPLAY EXAM
    # =========================================================

    return render(
        request,
        'students/take_exam.html',
        {
            'exam': exam,
            'participant': participant,
            'exam_questions': exam_questions,
        }
    )


@role_required('student')
@require_POST
def save_exam_answer(
    request,
    exam_id,
    exam_question_id
):

    participant = ConductedExamParticipant.objects.filter(
        exam_id=exam_id,
        student=request.user,
        status='ongoing',
    ).first()

    if participant is None:

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam is not active.'
            },
            status=403
        )


    exam_question = participant.exam.exam_questions.filter(
        id=exam_question_id
    ).select_related(
        'question'
    ).first()


    if exam_question is None:

        return JsonResponse(
            {
                'success': False,
                'error': 'Question not found.'
            },
            status=404
        )


    selected_option = request.POST.get(
        'selected_option',
        ''
    ).strip().upper()


    if selected_option not in [
        'A',
        'B',
        'C',
        'D'
    ]:

        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid option.'
            },
            status=400
        )


    answer, created = ConductedExamAnswer.objects.get_or_create(
        participant=participant,
        exam_question=exam_question,
    )


    answer.selected_option = selected_option

    answer.answered_at = timezone.now()

    answer.save(
        update_fields=[
            'selected_option',
            'answered_at',
            'updated_at',
        ]
    )


    return JsonResponse(
        {
            'success': True,
            'selected_option': selected_option,
        }
    )


@role_required('student')
def exam_waiting_status(request, exam_id):

    participant = ConductedExamParticipant.objects.filter(
        exam_id=exam_id,
        student=request.user,
    ).select_related('exam').first()

    if participant is None:

        return JsonResponse(
            {
                'success': False,
                'error': 'You have not joined this exam.'
            },
            status=403
        )


    exam = participant.exam


    return JsonResponse(
        {
            'success': True,
            'exam_status': exam.status,
        }
    )


@role_required('student')
def exam_submitted(request, exam_id):

    participant = ConductedExamParticipant.objects.filter(
        exam_id=exam_id,
        student=request.user,
        status__in=[
            'submitted',
            'auto_submitted',
        ],
    ).select_related('exam').first()

    if participant is None:

        messages.error(
            request,
            'Exam submission not found.'
        )

        return redirect(
            'student_join_exam'
        )

    return render(
        request,
        'students/exam_submitted.html',
        {
            'exam': participant.exam,
        }
    )