from django.contrib import admin
from .models import Task, Worker, Feedback

# Register your models here.
admin.site.register(Task)
admin.site.register(Worker)
admin.site.register(Feedback)