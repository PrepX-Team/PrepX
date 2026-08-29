from django import forms

from .models import ConductedExam


class ConductedExamForm(forms.ModelForm):

    negative_marks = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.01',
            'placeholder': 'Example: 0.50',
        }),
    )

    class Meta:
        model = ConductedExam
        fields = [
            'exam_name',
            'duration_minutes',
            'negative_marking_enabled',
            'negative_marks',
        ]

        widgets = {
            'exam_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter exam name',
            }),

            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Duration in minutes',
            }),

            'negative_marking_enabled': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        negative_enabled = cleaned_data.get(
            'negative_marking_enabled'
        )

        negative_marks = cleaned_data.get(
            'negative_marks'
        )

        if negative_enabled:

            if negative_marks is None or negative_marks <= 0:
                self.add_error(
                    'negative_marks',
                    'Enter negative marks greater than 0.'
                )

        else:
            cleaned_data['negative_marks'] = 0

        return cleaned_data