# Generated by Django 4.0.4 on 2022-06-16 05:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shift', '0006_alter_task_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
            preserve_default=False,
        ),
    ]
