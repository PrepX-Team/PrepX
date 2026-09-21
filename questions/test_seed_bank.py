"""Sanity checks for all seeded practice-question sets."""
from django.test import SimpleTestCase
from question_bank import GENERATORS, generate_questions


class QuestionBankTests(SimpleTestCase):
    def test_every_topic_has_ten_levels_of_25_valid_distinct_mcqs(self):
        for subject, topic in GENERATORS:
            for level in range(1, 11):
                with self.subTest(subject=subject, topic=topic, level=level):
                    questions = generate_questions(subject, topic, level)
                    self.assertEqual(len(questions), 25)
                    self.assertEqual(len({q['question_text'] for q in questions}), 25)
                    for question in questions:
                        self.assertIn(question['correct_option'], 'ABCD')
                        options = [question[f'option_{letter}'] for letter in 'abcd']
                        self.assertEqual(len(set(options)), 4)
                        self.assertTrue(question['explanation'])
