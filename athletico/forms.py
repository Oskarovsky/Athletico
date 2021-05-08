import logging

from django import forms
from django.shortcuts import render

from .firebase import firestore_db
from .models import Exercise, ExerciseType

logger = logging.getLogger(__name__)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('date', 'repetitions', 'exercise_type', 'weight', 'duration', 'handle_type')


class ExerciseTypeForm(forms.ModelForm):
    class Meta:
        model = ExerciseType
        fields = ['name']
