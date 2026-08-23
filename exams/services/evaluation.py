from ..models import ExamAnswer


def evaluate_answers(attempt):
    """
    Evaluate every assigned answer for an attempt.

    Returns:
        tuple: (correct_count, incorrect_count, unanswered_count)

    The ExamAttempt itself is not modified here.
    The caller is responsible for finalizing the attempt
    inside its transaction.
    """
    answers = attempt.answers.select_related('question')

    updated = []
    correct = 0
    incorrect = 0
    unanswered = 0

    for answer in answers:
        if answer.selected_option is None:
            answer.is_correct = None
            unanswered += 1

        elif answer.selected_option == answer.question.correct_option:
            answer.is_correct = True
            correct += 1

        else:
            answer.is_correct = False
            incorrect += 1

        updated.append(answer)

    if updated:
        ExamAnswer.objects.bulk_update(
            updated,
            ['is_correct'],
        )

    return correct, incorrect, unanswered


def calculate_score(correct_count):
    """
    Practice-test scoring rule:

    Correct     = +1
    Wrong       = 0
    Unanswered  = 0
    """
    return correct_count


def calculate_accuracy(correct_count, total_questions):
    """
    Return accuracy as a percentage rounded to two decimal places.
    """
    if total_questions == 0:
        return 0.0

    return round(
        (correct_count / total_questions) * 100,
        2,
    )