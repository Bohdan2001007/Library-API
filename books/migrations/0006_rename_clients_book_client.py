# Generated by Django 4.1.7 on 2023-03-21 15:25

from django.db import migrations
from django.core.management import call_command


def load_fixtures(state, schema_editor):
    call_command("loaddata", "Library_API.json.json")


def reverse_load_fixtures(state, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_borrowings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='clients',
            new_name='client',
        ),
    ]
