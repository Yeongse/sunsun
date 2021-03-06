# Generated by Django 4.0.4 on 2022-05-30 14:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('specification', models.TextField()),
                ('date', models.DateField()),
                ('startTime', models.IntegerField()),
                ('endTime', models.IntegerField()),
                ('type', models.CharField(max_length=64)),
                ('capacity', models.IntegerField()),
                ('extra', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(4)])),
                ('tasks', models.ManyToManyField(blank=True, related_name='workers', to='shift.task')),
            ],
        ),
    ]
