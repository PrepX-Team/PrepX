import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from exams.models import ExamAttempt

from .models import ExamLog


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