import logging

from django import forms
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from .models import Exercise, ExerciseType, BicepsSeries

logger = logging.getLogger(__name__)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('date', 'repetitions', 'exercise_type', 'weight', 'duration', 'handle_type')
        labels = {
            'date': _('DATA'),
            'repetitions': _('REPS'),
        }
        help_texts = {
            'date': _('Some useful help text.'),
        }
        widgets = {
            'date': TextInput(attrs={'placeholder': 'DATA'}),
        }


class ExerciseTypeForm(forms.ModelForm):
    class Meta:
        model = ExerciseType
        fields = ['name']


class BicepsSeriesForm(forms.ModelForm):
    class Meta:
        model = BicepsSeries
        fields = ('date', 'series_type',
                  'broken_bar_weight', 'broken_bar_repetitions',
                  'dumbbell_both_hands_weight', 'dumbbell_both_hands_repetitions',
                  'dumbbell_one_hand_max_weight', 'dumbbell_one_hand_max_repetitions')


class UpdateExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('date', 'repetitions', 'exercise_type', 'weight', 'duration', 'handle_type')
