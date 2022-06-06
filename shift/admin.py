from django.contrib import admin
from .models import Task, Worker, Feedback

# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    filter_horizontal = ("tasks", )

admin.site.register(Task)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Feedback)