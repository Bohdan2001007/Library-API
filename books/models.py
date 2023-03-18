from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    choice_of_cover = (
        ("H", "Hard"),
        ("S", "Soft"),
    )
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=30)
    cover = models.CharField(max_length=1, choices=choice_of_cover)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    Dailyfee = models.DecimalField(max_digits=4, decimal_places=2)
