from django import forms

from .models import Exercise, ExerciseType


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('date', 'repetitions', 'exercise_type', 'weight', 'duration')


class ExerciseTypeForm(forms.ModelForm):
    class Meta:
        model = ExerciseType
        fields = ['name']