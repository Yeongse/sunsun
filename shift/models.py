from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=64)
    specification = models.TextField()
    date = models.DateField()
    startTime = models.IntegerField()
    endTime = models.IntegerField()
    type = models.CharField(max_length=64)
    capacity = models.IntegerField()
    extra = models.TextField()

    def __str__(self):
        return f"{self.date} {self.name}"

class Worker(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(min_length=4, max_length=64)
    tasks = models.ManyToManyField(Task, blank=True, related_name="workers")

    def __str__(self):
        return f"{self.name} {self.email}"