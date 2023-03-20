from django.core.validators import MinValueValidator
from django.db import models
from borrowings.models import Borrowing


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
    clients = models.ManyToManyField('user.User', related_name='books')
    borrowings = models.ManyToManyField(Borrowing, related_name='books')

    class Meta:
        verbose_name = "Books"

    def __str__(self):
        return self.title
