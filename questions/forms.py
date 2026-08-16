from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = [
            'subject',
            'topic',
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_option',
            'explanation',
            'difficulty_level',
        ]

        widgets = {
            'correct_option': forms.Select(
                choices=[
                    ('A', 'A'),
                    ('B', 'B'),
                    ('C', 'C'),
                    ('D', 'D'),
                ]
            ),
        }

    def clean_difficulty_level(self):
        level = self.cleaned_data['difficulty_level']

        if not (1 <= level <= 10):
            raise forms.ValidationError(
                "Difficulty must be between 1 and 10."
            )

        return level

    def clean(self):
        cleaned_data = super().clean()

        subject = cleaned_data.get('subject')
        topic = cleaned_data.get('topic')

        if subject and topic and topic.subject_id != subject.id:
            raise forms.ValidationError(
                "The selected topic does not belong to the selected subject."
            )

        return cleaned_data