from django.shortcuts import render

from athletico.firebase import firestore_db
from athletico.forms import ExerciseForm


def home(request):
    context_dict = {'names_from_context': 'names_from_context'}
    return render(request, 'index.html', context_dict)


def show_stats(request):
    if request.method == "GET":
        exercise_ref = firestore_db.collection(u'exercise')
        docs = exercise_ref.stream()
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')

    return render(request, "stats.html")


def add_exercise(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        exercise_ref = firestore_db.collection(u'exercise')
        control_number = 2
        if form.is_valid():
            exercise = form.save(commit=False)
            is_exercise_ref = exercise_ref\
                .document(exercise.date.strftime("%Y-%m-%d"))\
                .collection("ex_type")\
                .document(exercise.type + "_" + str(control_number))

            is_exercise = is_exercise_ref.get().exists

            while is_exercise:
                control_number += 1
                is_exercise_ref = exercise_ref\
                    .document(exercise.date.strftime("%Y-%m-%d"))\
                    .collection("ex_type")\
                    .document(exercise.type + "_" + str(control_number))
                is_exercise = is_exercise_ref.get().exists

            exercise_ref\
                .document(exercise.date.strftime("%Y-%m-%d"))\
                .collection("ex_type")\
                .document(exercise.type + "_" + str(control_number)).set({
                    'date': exercise.date,
                    'type': exercise.type,
                    'weight': exercise.weight,
                    'duration': exercise.duration,
                    'repetitions': exercise.repetitions
                })
    else:
        form = ExerciseForm()
    return render(request, 'add_doc.html', {'form': form})

