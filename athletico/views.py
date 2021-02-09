import logging

from django.shortcuts import render
from django.utils import timezone

from athletico.firebase import firestore_db
from athletico.forms import ExerciseForm


def home(request):
    context_dict = {'names_from_context': 'names_from_context'}
    return render(request, 'index.html', context_dict)


def new_exercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            firestore_db.collection(u'exercise').doc('qwert').add({'date': exercise.date,
                                                      'type': exercise.type,
                                                      'weight': exercise.weight,
                                                      'duration': exercise.duration,
                                                      'repetitions': exercise.repetitions})
    else:
        form = ExerciseForm()
    return render(request, 'new_exercise.html', {'form': form})


def show_stats(request):
    if request.method == "GET":
        exercise_ref = firestore_db.collection(u'exercise')
        docs = exercise_ref.stream()
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')

    return render(request, "stats.html")


def add_doc(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        exercise_ref = firestore_db.collection(u'exercise')
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise_ref.document(exercise.date.strftime("%Y-%m-%d")).collection("ex_type").document(exercise.type).set({
                'date': exercise.date,
                'type': exercise.type,
                'weight': exercise.weight,
                'duration': exercise.duration,
                'repetitions': exercise.repetitions
            })

    else:
        form = ExerciseForm()
    return render(request, 'add_doc.html', {'form': form})

