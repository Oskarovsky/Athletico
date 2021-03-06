import base64
import io
import logging
import urllib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec

from django.shortcuts import render
from django.views.generic import FormView

from athletico import forms
from athletico.firebase import firestore_db
from athletico.forms import ExerciseForm, ExerciseTypeForm
from athletico.models import Exercise, EXERCISE_TYPES

figure, axes = plt.subplots(nrows=2, ncols=2)
gs = gridspec.GridSpec(2, 2)
figure.tight_layout(pad=3.5)

logger = logging.getLogger(__name__)


def home(request):
    context_dict = {'names_from_context': 'names_from_context'}
    return render(request, 'home.html', context_dict)


def show_stats(request, exercise_type):
    if request.method == "GET":
        plt.cla()
        plt.clf()
        exercise_types_list = []
        for exercise in EXERCISE_TYPES:
            exercise_types_list.append(exercise[0])
        exercise_type_form = ExerciseTypeForm
        ex_type = str(exercise_type).replace("-", " ")
        print(f"FETCHING INFORMATION ABOUT EXERCISE: {ex_type}")
        exercise_array = get_exercise_by_type(exercise_type)
        exercises_on_time = []
        if exercise_array in exercises_on_time:
            data = create_chart_for_duration(exercise_array)
        else:
            # Create 2x2 sub plots
            data = create_chart_for_weight(exercise_array)
            data = create_chart_for_repetitions(exercise_array)
            data = create_scatter_for_repetitions(exercise_array)
        graph = draw_graph(exercise_type)
    return render(request, "stats.html",
                  {'exercise_array': exercise_array,
                   'data': data,
                   'graph': graph,
                   'form': exercise_type_form,
                   'exe': exercise_types_list})


def draw_graph(exercise_type):
    exercise_array = get_exercise_by_type(exercise_type)
    repetitions_all, dates_all = [], []
    rep_right, dates_right = [], []
    rep_left, dates_left = [], []
    rep_both, dates_both = [], []
    for ex in exercise_array:
        repetitions_all.append(ex.repetitions)
        dates_all.append(str(ex.date).split(' ')[0])
        if ex.handle_type == 'right':
            rep_right.append(ex.repetitions)
            dates_right.append(str(ex.date).split(' ')[0])
        elif ex.handle_type == 'left':
            rep_left.append(ex.repetitions)
            dates_left.append(str(ex.date).split(' ')[0])
        else:
            rep_both.append(ex.repetitions)
            dates_both.append(str(ex.date).split(' ')[0])
    fig1, ax1 = plt.subplots()

    if repetitions_all:
        ax1.plot(dates_all, [int(x) for x in repetitions_all], label='All')
    if rep_right:
        ax1.plot(dates_right, [int(x) for x in rep_right], label='Right')
    if rep_left:
        ax1.plot(dates_left, [int(x) for x in rep_left], label='Left')
    if rep_both:
        ax1.plot(dates_both, [int(x) for x in rep_both], label='None/Both')

    plt.legend(loc='upper left')
    plt.grid(True, linewidth=0.2, color='#aaaaaa', linestyle='-')
    plt.title('REPETITIONS OF THE EXERCISE', fontweight='semibold')
    plt.ylabel('Date', size=12, fontweight='semibold')
    plt.xlabel('Repetitions', size=12, fontweight='semibold')
    plt.ylim(0)
    fig1 = plt.gcf()
    buf = io.BytesIO()
    fig1.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


def get_exercise_by_type(exercise_type):
    root_collection = firestore_db.collection(u'exercise').get()
    exercise_array = []
    for exercise_collection in root_collection:
        exercises = firestore_db.collection(u'exercise').document(f'{exercise_collection.id}').collection("ex_type") \
            .where(u'type', u'==', exercise_type).stream()
        for ex in exercises:
            print(f'{exercise_type} >>> TRAINING DAY -- {exercise_collection.id}')
            ex_date = u'{}'.format(ex.to_dict()['date'])
            ex_repetitions = u'{}'.format(ex.to_dict()['repetitions'])
            if ex.to_dict().get('handle'):
                ex_handle = u'{}'.format(ex.to_dict()['handle'])
            else:
                ex_handle = 'none'
            ex_weight = u'{}'.format(ex.to_dict()['weight'])
            ex_duration = u'{}'.format(ex.to_dict()['duration'])
            ex_type = u'{}'.format(ex.to_dict()['type'])

            exercise_array.append(Exercise(ex_date, ex_repetitions, ex_weight, ex_duration, ex_handle, ex_type))
            print(f' EXERCISE -- {ex.id} => {ex.to_dict()}\n ===============')
    print(f'Sum of fetched exercises: {len(exercise_array)}')
    return exercise_array


def create_chart_for_repetitions(exercise_array):
    repetitions = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        repetitions.append(ex.repetitions)
        dates.append(str(ex.date).split(' ')[0])
        iterator += 1
    plt.title('REPETITIONS CHAR')
    plt.subplot(gs[0, 0])  # row 0, col 0    plt.title('REPETITIONS')
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


def create_scatter_for_repetitions(exercise_array):
    repetitions = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        repetitions.append(ex.repetitions)
        dates.append(str(ex.date).split(' ')[0])
        iterator += 1
    plt.subplot(gs[1, :])  # row 1, span all columns
    plt.title('REPETITIONS')
    plt.plot(dates, repetitions, '-o')
    plt.xticks(dates, fontweight='bold', color='black', fontsize='7', horizontalalignment='center', rotation=30)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


def create_chart_for_weight(exercise_array):
    weight = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        weight.append(ex.weight)
        dates.append(str(ex.date).split(' ')[0])
        iterator += 1
    plt.subplot(gs[0, 1])  # row 0, col 1
    plt.title('WEIGHT')
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


def create_chart_for_duration(exercise_array):
    duration = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        duration.append(ex.duration)
        dates.append(str(ex.date).split(' ')[0])
        iterator += 1
    plt.subplot(1, 2, 1)
    plt.title('DURATION')
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


class StatsView:
    template_name = 'stats.html'
    success_url = '/'


class AddExerciseView(FormView):
    template_name = 'add_exercise.html'
    form_class = forms.ExerciseForm
    success_url = '/'

    def add_exercise(request):
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
                    'handle': exercise.handle_type,
                    'weight': exercise.weight,
                    'duration': exercise.duration,
                    'repetitions': exercise.repetitions
                })
                exercise_ref.document(exercise.date.strftime("%Y-%m-%d")).set({u'date': exercise.date})
        else:
            form = ExerciseForm
        return render(request, 'add_exercise.html', {'form': form})
