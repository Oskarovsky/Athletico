from django.shortcuts import render

from athletico.firebase import firestore_db
from athletico.forms import ExerciseForm
from athletico.models import Exercise

import io
import urllib, base64
import matplotlib.pyplot as plt


def home(request):
    context_dict = {'names_from_context': 'names_from_context'}
    return render(request, 'index.html', context_dict)


def show_stats(request):
    if request.method == "GET":
        exercise_array = get_exercise_from_db()
        uri = create_chart()
    return render(request, "stats.html", {'exercise_array': exercise_array, 'data': uri})


def get_exercise_from_db():
    docs = firestore_db.collection(u'exercise').get()
    exercise_array = []
    for doc in docs:
        print('============')
        print(f'TRAINING DAY -- {doc.id} => {doc.to_dict()}')
        cols = firestore_db.collection(u'exercise').document(f'{doc.id}').collection("ex_type").stream()
        print(f'READ ALL EXERCISES FROM {doc.id}')
        for col in cols:
            ex_date = u'{}'.format(col.to_dict()['date'])
            ex_repetitions = u'{}'.format(col.to_dict()['repetitions'])
            ex_weight = u'{}'.format(col.to_dict()['weight'])
            ex_duration = u'{}'.format(col.to_dict()['duration'])
            ex_type = u'{}'.format(col.to_dict()['type'])

            exercise_array.append(Exercise(ex_date, ex_repetitions, ex_weight, ex_duration, ex_type))
            print(f' EXERCISE -- {col.id} => {col.to_dict()}')
    print(f'Sum of fetched exercises: {len(exercise_array)}')
    print(exercise_array[0].date)
    return exercise_array


def create_chart():
    plt.plot(range(10))
    plt.xlabel('xlabel(X)')

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

def get_exercise_by_type(request):
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
        control_number = 0
        if form.is_valid():
            exercise = form.save(commit=False)
            is_exercise_ref = exercise_ref\
                .document(exercise.date.strftime("%Y-%m-%d"))\
                .collection("ex_type")\
                .document(exercise.exercise_type + "_" + str(control_number))

            is_exercise = is_exercise_ref.get().exists

            while is_exercise:
                control_number += 1
                is_exercise_ref = exercise_ref\
                    .document(exercise.date.strftime("%Y-%m-%d"))\
                    .collection("ex_type")\
                    .document(exercise.exercise_type + "_" + str(control_number))
                is_exercise = is_exercise_ref.get().exists

            exercise_ref\
                .document(exercise.date.strftime("%Y-%m-%d"))\
                .collection("ex_type")\
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
    return render(request, 'add_doc.html', {'form': form})

