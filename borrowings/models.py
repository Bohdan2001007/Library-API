from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ManyToManyField('books.Book')
    clients = models.ManyToManyField('user.User', related_name='borrowings')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.borrow_date} - {self.expected_return_date} - {self.actual_return_date}"
