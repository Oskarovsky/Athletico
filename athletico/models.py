from django.db import models

EXERCISE_TYPES = [
    ("crunches", "crunches"),  # brzuszki
    ("twisted crunches", "twisted crunches"),  # skrętobrzuszki
    ("plank", "plank"),  # deska
    ("bends", "bends"),  # skłony - unoszenie rąk i nóg (leżąc)
    ("leg lifting", "leg lifting"),  # podnoszenie nogi
    ("bicycle kick", "bicycle kick"),  # rowerek

    ("push-ups", "push-ups"),  # pompki
    ("dead bug", "dead bug"),  # marty robak
    ("cable crunch", "cable crunch"),  # spięcia

    ("moving the barbell", "moving the barbell"),  # Podnoszenie sztangi
    ("barbell press behind neck", "barbell press behind neck"),  # Wyciskanie sztangielki zza głowy (triceps)
    ("standing barbell curl", "standing barbell curl"),  # Uginanie ramion ze sztangą stojąc podchwytem
    ("standing dumbbell curl", "standing dumbbell curl"),  # HANTEL / STÓJKA -  Uginanie ramion ze sztangielkami stojąc podchwytem
    ("standing hammer curl", "standing hammer curl"),  # Uginanie ramion ze sztangielkami stojąc (uchwyt "młotkowy")
    ("concentration curl", "concentration curl"),  # HANTEL / KOLANO -  Uginanie ramienia ze sztangielką w siadzie - podpora o kolano
    ("EZ bar curl", "EZ bar curl"),  # GRYF ŁAMANY / STÓJKA - Uginanie ramion ze sztangą łamaną, stojąc
    ("bench dips", "bench dips"),  # Pompki w podporze tyłem (triceps)

    ("dumbbell flys", "dumbbell flys"),  # Rozpiętki ze sztangielkami leżąc na ławce poziomej
    ("barbell bench press", "barbell bench press"),  # GRYF / KLATKA -- Wyciskanie sztangi leżąc na ławce poziomej
    ("palms in dumbbell bench press", "palms in dumbbell bench press"),  # Wyciskanie sztangielek leżąc na ławce poziomej chwytem młotkowym
    ("dumbbell lateral raise", "dumbbell lateral raise")  # Unoszenie sztangielek bokiem w górę (barki)
]

HANDLE_TYPES = [
    ("right", "right"),
    ("left", "left"),
    ("both", "both"),
    ("none", "none")
]

SERIES_TYPES = [
    ("biceps_series", "biceps_series")
]


class Exercise(models.Model):

    def __init__(self):
        super().__init__()

    def __init__(self, date=None, repetitions=None, weight=None, duration=None, handle_type=None, exercise_type=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date
        self.repetitions = repetitions
        self.weight = weight
        self.duration = duration
        self.handle_type = handle_type
        self.exercise_type = exercise_type

    date = models.DateTimeField()
    repetitions = models.IntegerField()
    weight = models.FloatField()
    duration = models.FloatField()
    handle_type = models.CharField(max_length=10, choices=HANDLE_TYPES)
    exercise_type = models.CharField(max_length=40, choices=EXERCISE_TYPES)


class ExerciseType(models.Model):
    name = models.CharField(max_length=40, choices=EXERCISE_TYPES)


class BicepsSeries(models.Model):

    def __init__(self):
        super().__init__()

    def __init__(self, date=None, series_type=None,
                 broken_bar_weight=None, broken_bar_repetitions=None,
                 dumbbell_both_hands_weight=None, dumbbell_both_hands_repetitions=None,
                 dumbbell_one_hand_max_weight=None, dumbbell_one_hand_max_repetitions=None,
                 *args, **kwargs):
        self.date = date
        self.series_type = series_type
        self.broken_bar_weight = broken_bar_weight
        self.broken_bar_repetitions = broken_bar_repetitions
        self.dumbbell_both_hands_weight = dumbbell_both_hands_weight
        self.dumbbell_both_hands_repetitions = dumbbell_both_hands_repetitions
        self.dumbbell_one_hand_max_weight = dumbbell_one_hand_max_weight
        self.dumbbell_one_hand_max_repetitions = dumbbell_one_hand_max_repetitions

    date = models.DateTimeField()
    series_type = models.CharField(max_length=20, choices=SERIES_TYPES)
    broken_bar_weight = models.IntegerField()
    broken_bar_repetitions = models.IntegerField()
    dumbbell_both_hands_weight = models.IntegerField()
    dumbbell_both_hands_repetitions = models.IntegerField()
    dumbbell_one_hand_max_weight = models.IntegerField()
    dumbbell_one_hand_max_repetitions = models.IntegerField()


class HandleType(models.Model):
    name = models.CharField(max_length=10, choices=HANDLE_TYPES)
