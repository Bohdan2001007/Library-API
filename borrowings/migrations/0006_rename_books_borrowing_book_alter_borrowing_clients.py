# Generated by Django 4.1.7 on 2023-03-21 14:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('borrowings', '0005_rename_book_borrowing_books_alter_borrowing_clients'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowing',
            old_name='books',
            new_name='book',
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='clients',
            field=models.ManyToManyField(related_name='borrowings', to=settings.AUTH_USER_MODEL),
        ),
    ]
