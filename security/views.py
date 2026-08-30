import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from exams.models import ExamAttempt

from .models import ExamLog
#teacher exam log security import
from django.http import JsonResponse
from django.db import transaction
from django.db.models import F
from django.views.decorators.http import require_POST

from accounts.decorators import role_required

from teachers.models import ConductedExamParticipant

from .models import ConductedExamSecurityLog


ALLOWED_EVENTS = {
    choice[0]
    for choice in ExamLog.EventType.choices
}


@role_required('student')
@require_POST
def log_security_event(request, attempt_id):
    attempt = ExamAttempt.objects.filter(
        pk=attempt_id,
        student=request.user,
    ).first()

    if attempt is None:
        return JsonResponse(
            {
                'success': False,
                'error': 'Attempt not found.',
            },
            status=403,
        )

    try:
        payload = json.loads(request.body)
        event_type = payload.get('event_type')
    except (TypeError, json.JSONDecodeError):
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid request.',
            },
            status=400,
        )

    if event_type not in ALLOWED_EVENTS:
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid event type.',
            },
            status=400,
        )

    ExamLog.objects.create(
        attempt=attempt,
        event_type=event_type,
    )

    return JsonResponse({
        'success': True,
    })


@role_required('student')
@require_POST
def log_exam_security_event(request, exam_id):

    participant = ConductedExamParticipant.objects.filter(
        exam_id=exam_id,
        student=request.user,
        status='ongoing',
    ).first()

    if participant is None:

        return JsonResponse(
            {
                'success': False,
                'error': 'Exam is not active.',
            },
            status=403,
        )


    event_type = request.POST.get(
        'event_type',
        ''
    ).strip()


    allowed_events = {
        ConductedExamSecurityLog.EventType.TAB_SWITCH,
        ConductedExamSecurityLog.EventType.WINDOW_BLUR,
        ConductedExamSecurityLog.EventType.FULLSCREEN_EXIT,
        ConductedExamSecurityLog.EventType.COPY_ATTEMPT,
        ConductedExamSecurityLog.EventType.PASTE_ATTEMPT,
        ConductedExamSecurityLog.EventType.RIGHT_CLICK,
        ConductedExamSecurityLog.EventType.MINIMIZE_ATTEMPT,
        ConductedExamSecurityLog.EventType.KEYBOARD_ATTEMPT,
    }


    if event_type not in allowed_events:

        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid security event.',
            },
            status=400,
        )


    with transaction.atomic():

        ConductedExamSecurityLog.objects.create(
            participant=participant,
            event_type=event_type,
        )


        ConductedExamParticipant.objects.filter(
            pk=participant.pk,
        ).update(
            violation_count=F('violation_count') + 1,
        )


    return JsonResponse(
        {
            'success': True,
            'event_type': event_type,
        }
    )