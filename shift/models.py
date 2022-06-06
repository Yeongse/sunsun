from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=64)
    specification = models.TextField()
    date = models.DateField()
    startTime = models.CharField(max_length=6)
    endTime = models.CharField(max_length=6)
    type = models.CharField(max_length=64)
    capacity = models.IntegerField()
    extra = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} {self.name}"

class Worker(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(validators=[MinLengthValidator(4)], max_length=128)
    is_admin = models.BooleanField()
    tasks = models.ManyToManyField(Task, blank=True, related_name="workers")

    def __str__(self):
        return f"{self.name} {self.email}"

class Feedback(models.Model):
    text = models.TextField()
    response = models.TextField(blank=True, null=True)