# Generated by Django 4.0.4 on 2022-06-04 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shift', '0004_alter_worker_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('response', models.TextField(blank=True, null=True)),
            ],
        ),
    ]