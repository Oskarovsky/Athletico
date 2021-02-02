from django.db import models


class Exercise(models.Model):
    date = models.DateTimeField()
    repetitions = models.IntegerField()
    type = models.TextField()
    weight = models.FloatField()
    duration = models.FloatField()
