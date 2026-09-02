from exams.models import ExamAttempt, ExamAnswer

from core.constants import (
    MIN_TOPIC_ATTEMPTS_FOR_ANALYTICS,
    TREND_THRESHOLD_PERCENT,
    TREND_WINDOW_SIZE,
)


def _student_practice_attempts(student):
    """
    Return finalized practice attempts for the student.

    Conducted-exam attempts are excluded because ExamAttempt is also
    used by the conducted-exam system.
    """
    return ExamAttempt.objects.filter(
        student=student,
        status='submitted',
        exam__isnull=True,
    )


def student_overview(student):
    attempts = _student_practice_attempts(student)

    total = attempts.count()

    if total == 0:
        return {
            'has_data': False,
        }

    scores = [
        attempt.score
        for attempt in attempts
        if attempt.score is not None
    ]

    accuracies = [
        attempt.accuracy
        for attempt in attempts
        if attempt.accuracy is not None
    ]

    average_score = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    overall_accuracy = (
        sum(accuracies) / len(accuracies)
        if accuracies
        else 0
    )

    answers = ExamAnswer.objects.filter(
        attempt__in=attempts
    )

    correct = answers.filter(
        is_correct=True
    ).count()

    incorrect = answers.filter(
        is_correct=False,
        selected_option__isnull=False,
    ).count()

    unanswered = answers.filter(
        selected_option__isnull=True
    ).count()

    return {
        'has_data': True,
        'completed_tests': total,
        'average_score': round(average_score, 2),
        'overall_accuracy': round(overall_accuracy, 2),
        'correct': correct,
        'incorrect': incorrect,
        'unanswered': unanswered,
    }


def topic_analytics(student):
    attempts = (
        _student_practice_attempts(student)
        .select_related('topic')
        .order_by('start_time')
    )

    by_topic = {}

    for attempt in attempts:
        if attempt.topic_id is None:
            continue

        by_topic.setdefault(
            attempt.topic,
            [],
        ).append(attempt)

    results = []

    for topic, topic_attempts in by_topic.items():
        accuracies = [
            attempt.accuracy or 0
            for attempt in topic_attempts
        ]

        average_accuracy = (
            sum(accuracies) / len(accuracies)
            if accuracies
            else 0
        )

        attempt_count = len(topic_attempts)

        results.append({
            'topic': topic.name,
            'attempts': attempt_count,
            'accuracy': round(average_accuracy, 2),
            'sufficient_data': (
                attempt_count >=
                MIN_TOPIC_ATTEMPTS_FOR_ANALYTICS
            ),
        })

    return sorted(
        results,
        key=lambda result: result['accuracy'],
    )


def difficulty_analytics(student):
    """
    Practice tests are ordered by difficulty using test_number 1-10.
    Therefore test_number represents the difficulty level for
    practice analytics.
    """
    attempts = _student_practice_attempts(student)

    by_level = {}

    for attempt in attempts:
        if attempt.test_number is None:
            continue

        by_level.setdefault(
            attempt.test_number,
            [],
        ).append(attempt)

    results = []

    for level, level_attempts in sorted(
        by_level.items()
    ):
        accuracies = [
            attempt.accuracy or 0
            for attempt in level_attempts
        ]

        average_accuracy = (
            sum(accuracies) / len(accuracies)
            if accuracies
            else 0
        )

        results.append({
            'difficulty': level,
            'attempts': len(level_attempts),
            'accuracy': round(
                average_accuracy,
                2,
            ),
        })

    return results


def time_analytics(student):
    attempts = _student_practice_attempts(student).filter(
        end_time__isnull=False,
        start_time__isnull=False,
    )

    attempt_list = list(attempts)

    if not attempt_list:
        return {
            'has_data': False,
        }

    total_seconds = sum(
        (
            attempt.end_time -
            attempt.start_time
        ).total_seconds()
        for attempt in attempt_list
    )

    average_seconds = (
        total_seconds /
        len(attempt_list)
    )

    return {
        'has_data': True,
        'average_time_seconds': round(
            average_seconds,
            1,
        ),
        'total_tests': len(attempt_list),
    }


def weak_strong_topics(student):
    topics = [
        topic
        for topic in topic_analytics(student)
        if topic['sufficient_data']
    ]

    weak = [
        topic
        for topic in topics
        if topic['accuracy'] < 60
    ]

    strong = [
        topic
        for topic in topics
        if topic['accuracy'] >= 80
    ]

    return {
        'weak': weak,
        'strong': strong,
    }


def trend(student):
    """
    Compare the most recent 5 completed practice attempts
    against the previous 5 completed practice attempts.

    Difference:
        > +5 percentage points -> improving
        < -5 percentage points -> declining
        otherwise -> stable
    """

    attempts = list(
        _student_practice_attempts(student)
        .order_by('-start_time')[
            :TREND_WINDOW_SIZE * 2
        ]
    )

    required_attempts = (
        TREND_WINDOW_SIZE * 2
    )

    if len(attempts) < required_attempts:
        return {
            'status': 'insufficient_data',
        }

    recent = attempts[
        :TREND_WINDOW_SIZE
    ]

    previous = attempts[
        TREND_WINDOW_SIZE:
    ]

    recent_avg = (
        sum(
            attempt.accuracy or 0
            for attempt in recent
        ) / TREND_WINDOW_SIZE
    )

    previous_avg = (
        sum(
            attempt.accuracy or 0
            for attempt in previous
        ) / TREND_WINDOW_SIZE
    )

    difference = (
        recent_avg -
        previous_avg
    )

    if difference > TREND_THRESHOLD_PERCENT:
        status = 'improving'
    elif difference < -TREND_THRESHOLD_PERCENT:
        status = 'declining'
    else:
        status = 'stable'

    return {
        'status': status,
        'recent_avg': round(
            recent_avg,
            2,
        ),
        'previous_avg': round(
            previous_avg,
            2,
        ),
    }