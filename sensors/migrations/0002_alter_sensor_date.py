# Generated by Django 4.1.2 on 2023-05-07 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
