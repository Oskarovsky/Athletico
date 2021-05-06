import logging

from django import forms
from django.shortcuts import render

from .firebase import firestore_db
from .models import Exercise, ExerciseType

logger = logging.getLogger(__name__)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('date', 'repetitions', 'exercise_type', 'weight', 'duration')

    def add_exercise(request):
        logger.info("Adding new exercise to firebase")
        if request.method == "POST":
            form = ExerciseForm(request.POST)
            exercise_ref = firestore_db.collection(u'exercise')
            control_number = 0
            if form.is_valid():
                exercise = form.save(commit=False)
                is_exercise_ref = exercise_ref \
                    .document(exercise.date.strftime("%Y-%m-%d")) \
                    .collection("ex_type") \
                    .document(exercise.exercise_type + "_" + str(control_number))

                is_exercise = is_exercise_ref.get().exists

                while is_exercise:
                    control_number += 1
                    is_exercise_ref = exercise_ref \
                        .document(exercise.date.strftime("%Y-%m-%d")) \
                        .collection("ex_type") \
                        .document(exercise.exercise_type + "_" + str(control_number))
                    is_exercise = is_exercise_ref.get().exists

                exercise_ref \
                    .document(exercise.date.strftime("%Y-%m-%d")) \
                    .collection("ex_type") \
                    .document(exercise.exercise_type + "_" + str(control_number)).set({
                    'date': exercise.date,
                    'type': exercise.exercise_type,
                    'weight': exercise.weight,
                    'duration': exercise.duration,
                    'repetitions': exercise.repetitions
                })
                exercise_ref.document(exercise.date.strftime("%Y-%m-%d")).set({u'date': exercise.date})
        else:
            form = ExerciseForm
        return render(request, 'add_exercise.html', {'form': form})


class ExerciseTypeForm(forms.ModelForm):
    class Meta:
        model = ExerciseType
        fields = ['name']
