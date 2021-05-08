from django.db import models

EXERCISE_TYPES = [
    ("crunches", "crunches"),  # brzuszki
    ("twisted crunches", "twisted crunches"),  # skrętobrzuszki
    ("plank", "plank"),  # deska
    ("oblique glute bridges", "oblique glute bridges"),  # skośny mostek biodrowy
    ("simple glute bridges", "simple glute bridges"),  # prosty mostek biodrowy
    ("push-ups", "push-ups"),  # pompki
    ("cable crunch", "cable crunch"),  # spięcia
    ("lying floor legs and arms raise", "lying floor legs and arms raise"),  # unoszenie rąk i nóg (leżąc)
    ("barbell bench press", "barbell bench press"),  # Wyciskanie sztangielki leżąc na ławce poziomej
    ("dumbbell flys", "dumbbell flys"),  # Rozpiętki ze sztangielkami leżąc na ławce poziomej
    ("palms in dumbbell bench press", "palms in dumbbell bench press"),
    # Wyciskanie sztangielek leżąc na ławce poziomej chwytem młotkowym
    ("moving the barbell", "moving the barbell"),  # Podnoszenie sztangi
    ("barbell press behind neck", "barbell press behind neck"),  # Wyciskanie sztangielki zza głowy
    ("standing barbell curl", "standing barbell curl"),  # Uginanie ramion ze sztangą stojąc podchwytem
    ("standing dumbbell curl", "standing dumbbell curl"),  # Uginanie ramion ze sztangielkami stojąc podchwytem
    ("standing hammer curl", "standing hammer curl"),  # Uginanie ramion ze sztangielkami stojąc (uchwyt "młotkowy")
    ("concentration curl", "concentration curl"),  # Uginanie ramienia ze sztangielką w siadzie - podpora o kolano
    ("EZ bar curl", "EZ bar curl"),  # Uginanie ramion ze sztangą łamaną, stojąc
    ("seated french press", "seated french press"),  # Wyciskanie "francuskie" sztangielki w siadzie (triceps)
    ("bench dips", "bench dips")  # Pompki w podporze tyłem (triceps)
]

HANDLE_TYPES = [
    ("right", "right"),
    ("left", "left"),
    ("both", "both"),
    ("none", "none")
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


class HandleType(models.Model):
    name = models.CharField(max_length=10, choices=HANDLE_TYPES)
