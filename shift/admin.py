from django.contrib import admin
from .models import Task, Worker

# Register your models here.
admin.site.register(Task)
admin.site.register(Worker)