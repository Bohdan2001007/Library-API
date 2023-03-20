# Generated by Django 4.1.7 on 2023-03-19 17:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('borrowings', '0002_borrowing_book'),
        ('books', '0002_alter_book_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='borrowings',
            field=models.ManyToManyField(related_name='books', to='borrowings.borrowing'),
        ),
        migrations.AddField(
            model_name='book',
            name='clients',
            field=models.ManyToManyField(related_name='books', to=settings.AUTH_USER_MODEL),
        ),
    ]