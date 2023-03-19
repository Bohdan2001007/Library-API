# Generated by Django 4.1.7 on 2023-03-18 14:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=30)),
                ('cover', models.CharField(choices=[('H', 'Hard'), ('S', 'Soft')], max_length=1)),
                ('inventory', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('Dailyfee', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]