from django.shortcuts import render
from django.utils import timezone

from athletico.firebase import firestore_db
from athletico.forms import ExerciseForm


def home(request):
    # add_exercise()
    context_dict = {'names_from_context': 'names_from_context'}
    return render(request, 'index.html', context_dict)


def new_exercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.date = timezone.now()
            firestore_db.collection(u'exercise').add({'date': exercise.date, 'type': exercise.type,
                                                      'weight': exercise.weight, 'duration': exercise.duration,
                                                      'repetitions': exercise.repetitions})
    else:
        form = ExerciseForm()
    return render(request, 'new_exercise.html', {'form': form})
