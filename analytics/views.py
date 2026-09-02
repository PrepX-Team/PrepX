from django.shortcuts import render

from accounts.decorators import role_required

from . import services


@role_required('student')
def student_analytics(request):
    student = request.user

    return render(
        request,
        'analytics/student.html',
        {
            'overview': services.student_overview(student),
            'topics': services.topic_analytics(student),
            'difficulty': services.difficulty_analytics(student),
            'time': services.time_analytics(student),
            'weak_strong': services.weak_strong_topics(student),
            'trend': services.trend(student),
        },
    )