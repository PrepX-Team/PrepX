"""Add missing QA/LR questions for tests 1 to 10. Run: python seed_questions.py"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from questions.models import Question
from subjects.models import Subject, Topic
from question_bank import TOPICS, generate_questions


def seed():
    admin = get_user_model().objects.filter(is_superuser=True, is_active=True).first()
    if admin is None:
        raise RuntimeError('First create a superuser: python manage.py createsuperuser')

    total_created = 0

    for subject_name, topic_names in TOPICS.items():
        subject = Subject.objects.filter(name__iexact=subject_name, is_active=True).first()
        if subject is None:
            raise RuntimeError(f'Missing subject: {subject_name}')

        for topic_name in topic_names:
            topic = Topic.objects.filter(
                subject=subject, name__iexact=topic_name, is_active=True
            ).first()
            if topic is None:
                raise RuntimeError(f'Missing topic: {subject_name} / {topic_name}')

            for level in range(1, 11):
                questions = Question.objects.filter(
                    subject=subject, topic=topic, difficulty_level=level
                )
                existing_texts = set(questions.values_list('question_text', flat=True))
                eligible_count = questions.filter(
                    is_global=True, status='approved', is_active=True
                ).count()

                new_questions = []
                for data in generate_questions(subject_name, topic_name, level):
                    if eligible_count + len(new_questions) >= 25:
                        break
                    if data['question_text'] in existing_texts:
                        continue
                    new_questions.append(Question(
                        subject=subject, topic=topic, difficulty_level=level,
                        created_by=admin, is_global=True, status='approved',
                        **data,
                    ))
                    existing_texts.add(data['question_text'])

                Question.objects.bulk_create(new_questions)
                total_created += len(new_questions)
                final_count = eligible_count + len(new_questions)
                print(f'{subject_name} / {topic_name} / Test {level}: '
                      f'{len(new_questions)} added, {final_count} eligible')
                if final_count < 20:
                    raise RuntimeError(f'Not enough questions for {topic_name}, Test {level}')

    print(f'DONE: {total_created} questions created.')


if __name__ == '__main__':
    seed()
