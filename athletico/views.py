import base64
import io
import logging
import pdb
import urllib
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import gridspec, colors

from django.shortcuts import render
from django.views.generic import FormView
from matplotlib.ticker import MaxNLocator

from athletico import forms
from athletico.firebase import firestore_db
from athletico.forms import ExerciseForm, ExerciseTypeForm, BicepsSeriesForm
from athletico.models import Exercise, EXERCISE_TYPES, BicepsSeries

# pdb.set_trace()

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
        if exercise_type == 'plank':
            exercise_array = get_exercise_by_type(exercise_type)
            bar_graph_d2d = draw_bar_graph_duration_to_date(exercise_array)
            histogram_duration = draw_histogram_duration_onetime(exercise_array)
            return render(request, "stats.html",
                          {'exercise_array': exercise_array,
                           'bar_graph_d2d': bar_graph_d2d,
                           'histogram_duration': histogram_duration,
                           'form': exercise_type_form,
                           'exe': exercise_types_list})
        elif exercise_type == 'biceps_series':
            multi_bar_graph_biceps_series = draw_multi_bar_graph_biceps_series()
            return render(request, "stats.html",
                          {'multi_bar_graph_biceps_series': multi_bar_graph_biceps_series,
                           'form': exercise_type_form,
                           'exe': exercise_types_list})
        else:
            exercise_array = get_exercise_by_type(exercise_type)
            bar_graph_w2d = draw_bar_graph_weight_to_date(exercise_array)
            bar_graph_r2d = draw_bar_graph_repetitions_to_date(exercise_array)
            scatter_r2d = draw_scatter_repetitions_to_date(exercise_array)
            func_r2d = draw_graph(exercise_array)
            histogram_weight = draw_histogram_weight(exercise_array)
            return render(request, "stats.html",
                          {'exercise_array': exercise_array,
                           'scatter_r2d': scatter_r2d,
                           'bar_graph_w2d': bar_graph_w2d,
                           'bar_graph_r2d': bar_graph_r2d,
                           'func_r2d': func_r2d,
                           'histogram_weight': histogram_weight,
                           'form': exercise_type_form,
                           'exe': exercise_types_list})


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


def get_biceps_series():
    root_collection = firestore_db.collection(u'exercise').get()
    series_array = []
    for series_collection in root_collection:
        series = firestore_db.collection(u'exercise').document(f'{series_collection.id}').collection("series") \
            .where(u'series_type', u'==', 'biceps_series').stream()
        for ser in series:
            print(f'>>> TRAINING DAY SERIES -- {series_collection.id}')
            series_date = u'{}'.format(ser.to_dict()['date'])
            series_type = u'{}'.format(ser.to_dict()['series_type'])
            broken_bar_weight = u'{}'.format(ser.to_dict()['broken_bar_weight'])
            broken_bar_repetitions = u'{}'.format(ser.to_dict()['broken_bar_repetitions'])
            dumbbell_both_hands_weight = u'{}'.format(ser.to_dict()['dumbbell_both_hands_weight'])
            dumbbell_both_hands_repetitions = u'{}'.format(ser.to_dict()['dumbbell_both_hands_repetitions'])
            dumbbell_one_hand_max_weight = u'{}'.format(ser.to_dict()['dumbbell_one_hand_max_weight'])
            dumbbell_one_hand_max_repetitions = u'{}'.format(ser.to_dict()['dumbbell_one_hand_max_repetitions'])
            series_array.append(BicepsSeries(series_date, series_type,
                                             broken_bar_weight, broken_bar_repetitions,
                                             dumbbell_both_hands_weight, dumbbell_both_hands_repetitions,
                                             dumbbell_one_hand_max_weight, dumbbell_one_hand_max_repetitions))
    print(f'Sum of fetched series: {len(series_array)}')
    return series_array


def draw_graph(exercise_array):
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
        ax1.plot(dates_all, [int(x) for x in repetitions_all], label='All', color='b', linewidth=1)
    if rep_right:
        ax1.plot(dates_right, [int(x) for x in rep_right], label='Right', color='m', linewidth=0.7)
    if rep_left:
        ax1.plot(dates_left, [int(x) for x in rep_left], label='Left', color='r', linewidth=0.7)
    if rep_both:
        ax1.plot(dates_both, [int(x) for x in rep_both], label='None/Both', color='y', linewidth=0.7)

    ax1.spines['left'].set_linewidth(1.3)
    ax1.spines['left'].set_visible(True)
    ax1.spines['bottom'].set_linewidth(1.3)
    ax1.spines['bottom'].set_visible(True)
    ax1.spines['right'].set_linewidth(0.5)
    ax1.spines['right'].set_visible(True)
    ax1.spines['top'].set_linewidth(0.5)
    ax1.spines['top'].set_visible(True)
    plt.legend(loc='upper left')
    plt.grid(True, linewidth=0.2, color='#aaaaaa', linestyle='-')
    plt.title('REPETITIONS OF THE EXERCISE', fontweight='semibold')
    plt.ylabel('Repetitions', size=12, fontweight='semibold')
    plt.xlabel('Date', size=12, fontweight='semibold')
    plt.ylim(0)
    plt.xticks(fontweight='bold', color='black', fontsize='7', horizontalalignment='center', rotation=30)

    fig1 = plt.gcf()
    buf = io.BytesIO()
    fig1.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


def draw_multi_bar_graph_biceps_series():

    result_list = []
    iterator_date = []
    series_array = get_biceps_series()
    for series in series_array:
        iterator_date.append(series.date)
        iterator_list = [series.broken_bar_repetitions, series.dumbbell_both_hands_repetitions, series.dumbbell_one_hand_max_repetitions]
        result_list.append(iterator_list)
        print(f'x - {iterator_list[0]}, xx - {iterator_list[1]}, xxx - {iterator_list[2]}')

    fig_multi_bar_biceps_series, ax_multi_bar_biceps_series = plt.subplots()
    if result_list:
        df = pd.DataFrame(result_list)
        df.columns = ['Broken bar', 'Dumbbell both hands', 'Dumbbell one hand']
        df.index = [iterator_date]
        df = df.astype(float)
        df.plot(kind='bar', width=0.4)

    labels_biceps_series = ['Broken bar', 'Dumbbell both hands', 'Dumbbell one hand']
    plt.title('BICEPS SERIES', fontweight='semibold')
    plt.ylabel('Amount', size=12, fontweight='semibold')
    plt.xlabel('Weight', size=12, fontweight='semibold')
    plt.xticks(rotation=0)

    fig_multi_bar_biceps_series = plt.gcf()
    buf_multi_bar_biceps_series = io.BytesIO()
    fig_multi_bar_biceps_series.savefig(buf_multi_bar_biceps_series, format='png', dpi=300)
    buf_multi_bar_biceps_series.seek(0)
    string = base64.b64encode(buf_multi_bar_biceps_series.read())
    uri = urllib.parse.quote(string)
    return uri


def draw_bar_graph_repetitions_to_date(exercise_array):
    repetitions = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        repetitions.append(ex.repetitions)
        dates.append(str(ex.date).split(' ')[0])
        iterator += 1
    y_pos = np.arange(len(dates))

    fig_func_r2d, ax_func_r2d = plt.subplots()
    plt.title('REPETITIONS TO DATE BAR GRAPH', fontweight='semibold')
    plt.ylabel('Repetitions', size=12, fontweight='semibold')
    plt.xlabel('Date', size=12, fontweight='semibold')
    plt.bar(y_pos, [int(x) for x in repetitions], align='center', alpha=0.5)
    plt.xticks(y_pos, dates, fontweight='bold', color='orange', fontsize='7', horizontalalignment='center', rotation=30)

    fig_func_r2d = plt.gcf()
    buf_func_r2d = io.BytesIO()
    fig_func_r2d.savefig(buf_func_r2d, format='png', dpi=300)
    buf_func_r2d.seek(0)
    string = base64.b64encode(buf_func_r2d.read())
    uri = urllib.parse.quote(string)
    return uri


def draw_histogram_weight(exercise_array):
    weight = []
    for ex in exercise_array:
        for x in range(int(ex.repetitions)):
            weight.append(float(ex.weight.split(".", 1)[0]))
    weight.sort()
    fig_histogram_weight, ax_histogram_weight = plt.subplots()
    ax_histogram_weight.yaxis.set_major_locator(MaxNLocator(integer=True))  # force Y axis to use only integers
    plt.title('HISTOGRAM WEIGHT', fontweight='semibold')
    plt.ylabel('Amount', size=12, fontweight='semibold')
    plt.xlabel('Weight', size=12, fontweight='semibold')

    if len(weight) > 0:
        # Freedman–Diaconis rule to be more scientific in choosing the "right" bin width:
        q25, q75 = np.percentile(weight, [.25, .75])
        bin_width = 2 * (q75 - q25) * len(weight) ** (-1 / 3)
        print(f'XX -- {bin_width} -- {max(weight)} - {min(weight)}')
        if not bin_width == 0:
            bins = round((max(weight) - min(weight)) // bin_width)
        else:
            bins = 100
        print("Freedman–Diaconis number of bins:", bins)

        # N is the count in each bin, bins is the lower-limit of the bin
        N, bins, patches = plt.hist(weight, density=False, bins=bins)

        # We'll color code by height, but you could use any scalar
        fracs = N / N.max()

        # we need to normalize the data to 0..1 for the full range of the colormap
        norm = colors.Normalize(fracs.min(), fracs.max())

        # Now, we'll loop through our objects and set the color of each accordingly
        for thisfrac, thispatch in zip(fracs, patches):
            color = plt.cm.viridis(norm(thisfrac))
            thispatch.set_facecolor(color)

    fig_histogram_weight = plt.gcf()
    buf_histogram_weight = io.BytesIO()
    fig_histogram_weight.savefig(buf_histogram_weight, format='png', dpi=300)
    buf_histogram_weight.seek(0)
    string = base64.b64encode(buf_histogram_weight.read())
    uri = urllib.parse.quote(string)
    return uri


def draw_histogram_duration_onetime(exercise_array):
    duration = []
    for ex in exercise_array:
        duration.append(float(ex.duration.split(".", 1)[0]))
    duration.sort()

    fig_histogram_duration_onetime, ax_histogram_duration_onetime = plt.subplots()
    ax_histogram_duration_onetime.yaxis.set_major_locator(MaxNLocator(integer=True))  # force Y axis to use only integers
    plt.title('HISTOGRAM WEIGHT', fontweight='semibold')
    plt.ylabel('Amount', size=12, fontweight='semibold')
    plt.xlabel('Weight', size=12, fontweight='semibold')

    if len(duration) > 0:
        # Freedman–Diaconis rule to be more scientific in choosing the "right" bin width:
        q25, q75 = np.percentile(duration, [.25, .75])
        bin_width = 2 * (q75 - q25) * len(duration) ** (-1 / 3)
        print(f'XX -- {bin_width} -- {max(duration)} - {min(duration)}')
        if not bin_width == 0:
            bins = round((max(duration) - min(duration)) // bin_width)
        else:
            bins = 100
        print("Freedman–Diaconis number of bins:", bins)

        # N is the count in each bin, bins is the lower-limit of the bin
        N, bins, patches = plt.hist(duration, density=False, bins=bins)

        # We'll color code by height, but you could use any scalar
        fracs = N / N.max()

        # we need to normalize the data to 0..1 for the full range of the colormap
        norm = colors.Normalize(fracs.min(), fracs.max())

        # Now, we'll loop through our objects and set the color of each accordingly
        for thisfrac, thispatch in zip(fracs, patches):
            color = plt.cm.viridis(norm(thisfrac))
            thispatch.set_facecolor(color)

    fig_histogram_duration_onetime = plt.gcf()
    buf_histogram_duration_onetime = io.BytesIO()
    fig_histogram_duration_onetime.savefig(buf_histogram_duration_onetime, format='png', dpi=300)
    buf_histogram_duration_onetime.seek(0)
    string = base64.b64encode(buf_histogram_duration_onetime.read())
    uri = urllib.parse.quote(string)
    return uri


def draw_bar_graph_weight_to_date(exercise_array):
    weight = []
    dates = []
    for ex in exercise_array:
        weight.append(ex.weight)
        dates.append(str(ex.date).split(' ')[0])
    y_pos = np.arange(len(dates))

    fig_graph_w2d, ax_graph_w2d = plt.subplots()
    plt.title('WEIGHT TO DATE FUNCTION', fontweight='semibold')
    plt.ylabel('Weight', size=12, fontweight='semibold')
    plt.xlabel('Date', size=12, fontweight='semibold')
    plt.bar(y_pos, [float(x) for x in weight], align='center', alpha=0.5)
    plt.xticks(y_pos, dates, fontweight='bold', color='black', fontsize='7', horizontalalignment='center', rotation=30)

    fig_graph_w2d = plt.gcf()
    buf_graph_w2d = io.BytesIO()
    fig_graph_w2d.savefig(buf_graph_w2d, format='png', dpi=300)
    buf_graph_w2d.seek(0)
    string = base64.b64encode(buf_graph_w2d.read())
    uri = urllib.parse.quote(string)
    return uri


def draw_scatter_repetitions_to_date(exercise_array):
    repetitions = []
    dates = []
    iterator = 0
    for ex in exercise_array:
        repetitions.append(ex.repetitions)
        dates.append(str(ex.date).split(' ')[0])
        iterator += 1

    fig_scatter_r2d, ax_scatter_r2d = plt.subplots()
    plt.title('REPETITIONS TO DATE SCATTER', fontweight='semibold')
    ax_scatter_r2d.plot(dates, repetitions, '-o')
    plt.ylabel('Repetitions', size=12, fontweight='semibold')
    plt.xlabel('Date', size=12, fontweight='semibold')
    plt.grid(True, linewidth=0.2, color='#aaaaaa', linestyle='-')
    plt.xticks(dates, fontweight='bold', color='black', fontsize='7', horizontalalignment='center', rotation=30)

    fig_scatter_r2d = plt.gcf()
    buf_scatter_r2d = io.BytesIO()
    fig_scatter_r2d.savefig(buf_scatter_r2d, format='png', dpi=300)
    buf_scatter_r2d.seek(0)
    string = base64.b64encode(buf_scatter_r2d.read())
    uri = urllib.parse.quote(string)
    return uri


def draw_bar_graph_duration_to_date(exercise_array):
    duration = []
    dates = []
    for ex in exercise_array:
        duration.append(ex.duration)
        dates.append(str(ex.date).split(' ')[0])
    y_pos = np.arange(len(dates))

    fig_graph_d2d, ax_graph_d2d = plt.subplots()
    plt.title('DURATION TO DATE GRAPH')
    plt.ylabel('Duration', size=12, fontweight='semibold')
    plt.xlabel('Date', size=12, fontweight='semibold')
    plt.bar(y_pos, [int(x.split('.')[0]) for x in duration], align='center', alpha=0.5)
    plt.xticks(y_pos, dates, fontweight='bold', color='black', fontsize='7', horizontalalignment='center', rotation=30)

    fig_graph_d2d = plt.gcf()
    buf_graph_d2d = io.BytesIO()
    fig_graph_d2d.savefig(buf_graph_d2d, format='png', dpi=300)
    buf_graph_d2d.seek(0)
    string = base64.b64encode(buf_graph_d2d.read())
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


class AddBicepsSeriesView(FormView):
    template_name = 'add_biceps_series.html'
    form_class = forms.BicepsSeriesForm
    success_url = '/'

    def add_exercise(request):
        if request.method == "POST":
            form = BicepsSeriesForm(request.POST)
            exercise_ref = firestore_db.collection(u'exercise')
            control_number = 0
            if form.is_valid():
                exercise = form.save(commit=False)
                is_exercise_ref = exercise_ref \
                    .document(exercise.date.strftime("%Y-%m-%d")) \
                    .collection("series") \
                    .document("biceps_series_" + str(control_number))
                is_exercise = is_exercise_ref.get().exists

                while is_exercise:
                    control_number += 1
                    is_exercise_ref = exercise_ref \
                        .document(exercise.date.strftime("%Y-%m-%d")) \
                        .collection("series") \
                        .document("biceps_series_" + str(control_number))
                    is_exercise = is_exercise_ref.get().exists

                exercise_ref \
                    .document(exercise.date.strftime("%Y-%m-%d")) \
                    .collection("series") \
                    .document("biceps_series_" + str(control_number)).set({
                    'date': exercise.date,
                    'series_type': exercise.series_type,
                    'broken_bar_weight': exercise.broken_bar_weight,
                    'broken_bar_repetitions': exercise.broken_bar_repetitions,
                    'dumbbell_both_hands_weight': exercise.dumbbell_both_hands_weight,
                    'dumbbell_both_hands_repetitions': exercise.dumbbell_both_hands_repetitions,
                    'dumbbell_one_hand_max_weight': exercise.dumbbell_one_hand_max_weight,
                    'dumbbell_one_hand_max_repetitions': exercise.dumbbell_one_hand_max_repetitions
                })
                exercise_ref.document(exercise.date.strftime("%Y-%m-%d")).set({u'date': exercise.date})
        else:
            form = BicepsSeriesForm
        return render(request, 'add_exercise.html', {'form': form})
