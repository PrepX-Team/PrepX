from django.db import models
from core.models import BaseModel
from exams.models import ExamAttempt


class ExamLog(BaseModel):
    class EventType(models.TextChoices):
        TAB_SWITCH = 'tab_switch', 'Tab Switch'
        WINDOW_BLUR = 'window_blur', 'Window Blur'
        FULLSCREEN_EXIT = 'fullscreen_exit', 'Fullscreen Exit'
        COPY_ATTEMPT = 'copy_attempt', 'Copy Attempt'
        PASTE_ATTEMPT = 'paste_attempt', 'Paste Attempt'
        RIGHT_CLICK = 'right_click', 'Right Click'
        IDLE = 'idle', 'Idle'
        RAPID_ANSWER = 'rapid_answer', 'Rapid Answer'

    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='logs')
    event_type = models.CharField(max_length=30, choices=EventType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)  # server-authoritative, ignores client time

    class Meta:
        indexes = [models.Index(fields=['attempt']), models.Index(fields=['event_type'])]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.attempt.pk} - {self.event_type}"

class ConductedExamSecurityLog(BaseModel):

    class EventType(models.TextChoices):
        TAB_SWITCH = 'tab_switch', 'Tab Switch'
        WINDOW_BLUR = 'window_blur', 'Window Blur'
        FULLSCREEN_EXIT = 'fullscreen_exit', 'Fullscreen Exit'
        COPY_ATTEMPT = 'copy_attempt', 'Copy Attempt'
        PASTE_ATTEMPT = 'paste_attempt', 'Paste Attempt'
        RIGHT_CLICK = 'right_click', 'Right Click'
        MINIMIZE_ATTEMPT = 'minimize_attempt', 'Minimize Attempt'
        KEYBOARD_ATTEMPT = 'keyboard_attempt', 'Keyboard Attempt'

    participant = models.ForeignKey(
        'teachers.ConductedExamParticipant',
        on_delete=models.CASCADE,
        related_name='security_logs',
    )

    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=['participant', 'timestamp']
            ),
            models.Index(
                fields=['event_type']
            ),
        ]

        ordering = ['-timestamp']

    def __str__(self):
        return (
            f"{self.participant.student.username} - "
            f"{self.event_type}"
        )