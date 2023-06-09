# Generated by Django 4.1.7 on 2023-03-20 21:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('borrowings', '0003_alter_borrowing_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='clients',
            field=models.ManyToManyField(related_name='borrowings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='borrowing',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
