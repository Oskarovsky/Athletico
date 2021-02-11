import base64
import io
import urllib

import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render
from matplotlib import gridspec

from athletico.firebase import firestore_db
from athletico.forms import ExerciseForm
from athletico.models import Exercise

figure, axes = plt.subplots(nrows=2, ncols=2)
gs = gridspec.GridSpec(2, 2)
figure.tight_layout(pad=3.5)


def home(request):
    context_dict = {'names_from_context': 'names_from_context'}
    return render(request, 'index.html', context_dict)


def show_stats(request, exercise_type):
    if request.method == "GET":
        plt.cla()
        ex_type = str(exercise_type).replace("-", " ")
        print(f"FETCHING INFORMATION ABOUT EXERCISE: {ex_type}")
        exercise_array = get_exercise_from_db()
        exercises_on_time = []
        if exercise_array in exercises_on_time:
            data = create_chart_for_duration(exercise_array, ex_type)
        else:
            # Create 2x2 sub plots
            data = create_chart_for_weight(exercise_array, ex_type)
            data = create_chart_for_repetitions(exercise_array, ex_type)
            data = create_scatter_for_repetitions(exercise_array, ex_type)
    return render(request, "stats.html", {'exercise_array': exercise_array, 'data': data})


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


def create_chart_for_repetitions(exercise_array, exercise_type):
    plt.subplot(gs[0, 0])  # row 0, col 0    plt.title('REPETITIONS')
    repetitions = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        if ex.exercise_type == exercise_type:
            repetitions.append(ex.repetitions)
            dates.append(str(ex.date).split(' ')[0])
            iterator += 1
    y_pos = np.arange(len(dates))
    plt.bar(y_pos, [int(x) for x in repetitions], align='center', alpha=0.5)
    plt.xticks(y_pos, dates, fontweight='bold', color='orange', fontsize='7', horizontalalignment='center', rotation=30)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


def create_scatter_for_repetitions(exercise_array, exercise_type):
    plt.subplot(gs[1, :])  # row 1, span all columns
    plt.title('REPETITIONS')
    repetitions = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        if ex.exercise_type == exercise_type:
            repetitions.append(ex.repetitions)
            dates.append(str(ex.date).split(' ')[0])
            iterator += 1
    plt.plot(dates, repetitions, '-o')
    plt.show()

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


def create_chart_for_weight(exercise_array, exercise_type):
    plt.subplot(gs[0, 1]) # row 0, col 1
    plt.title('WEIGHT')
    weight = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        if ex.exercise_type == exercise_type:
            weight.append(ex.weight)
            dates.append(str(ex.date).split(' ')[0])
            iterator += 1
    y_pos = np.arange(len(dates))
    plt.bar(y_pos, [float(x) for x in weight], align='center', alpha=0.5)
    plt.xticks(y_pos, dates, fontweight='bold', color='black', fontsize='7', horizontalalignment='center', rotation=30)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


def create_chart_for_duration(exercise_array, exercise_type):
    plt.subplot(1, 2, 1)
    plt.title('DURATION')
    duration = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        if ex.exercise_type == exercise_type:
            duration.append(ex.duration)
            dates.append(str(ex.date).split(' ')[0])
            iterator += 1
    y_pos = np.arange(len(dates))
    plt.bar(y_pos, [int(x) for x in duration], align='center', alpha=0.5)
    plt.xticks(y_pos, dates, fontweight='bold', color='black', fontsize='7', horizontalalignment='center', rotation=30)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


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

