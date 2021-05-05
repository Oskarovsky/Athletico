from django.test import TestCase

from athletico import forms
from athletico.models import Exercise


class TestForm(TestCase):
    def test_valid_add_exercise(self):
        form = forms.ExerciseForm({
            Exercise(1, '2021-04-24', 10, 10, 0, "crunches")
        })
        # TODO self.assertTrue(form.is_valid())
