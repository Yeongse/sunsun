from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from tabnanny import check
from django.contrib.auth.hashers import make_password, check_password

from .models import Task, Worker, Feedback
from .forms import LoginForm, FeedbackForm

from django.views import generic


import datetime
now = datetime.datetime.now()

def login_checker(func):
    def checker(request, **kwargs):
        if "worker_id" not in request.session:
            return HttpResponseRedirect(reverse("shift:login"))
        else:
            return func(request, **kwargs)
    return checker

# Create your views here.
def login(request):
    err_message = ""
    if request.method ==  "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            input_name = form.cleaned_data["name"]
            input_password = form.cleaned_data["password"]
            matched_workers = Worker.objects.filter(name=input_name)

            # check username
            if len(matched_workers) == 0:
                err_message = "ユーザ名が正しくありません"
            else:
                worker = matched_workers[0]
                is_auth = check_password(input_password, worker.password)

                # check password
                if is_auth:
                    request.session["worker_id"] = worker.id
                    return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
                else:
                    err_message = "パスワードが正しくありません"            
       
    return render(request, "shift/login.html", {
        "message": err_message, 
        "form": LoginForm()
    })

@login_checker
def home(request, year, month):
    from . import mixins
    worker = Worker.objects.get(id=request.session["worker_id"])
    calendar = mixins.MonthCalendarMixin()
    calendar_data = calendar.get_month_calendar(year, month)

    month_days_tasks = []
    for week in calendar_data["month_days"]:
        week_days_tasks = []
        for day in week:
            day_tasks = Task.objects.filter(date=day)

            # 業務とそこで今のところ配属された人数をまとめて辞書で保存
            # jinjaの中でtask.workers.all()っていうクエリを書けへんかったからこうしてる
            task_and_members = []
            for task in day_tasks:
                task_and_members.append({"task": task, "member_num": len(task.workers.all())})

            day_days_tasks = {"day": day, "task_and_members": task_and_members }
            week_days_tasks.append(day_days_tasks)
        month_days_tasks.append(week_days_tasks)
    
    return render(request, "shift/home.html", {
        "calendar_data": calendar_data, 
        "month_days_tasks": month_days_tasks, 
        "worker": worker
    })

@login_checker
def specification(request, task_id):
    task = Task.objects.get(id=task_id)
    worker = Worker.objects.get(id=request.session["worker_id"])
    
    if request.method == "POST":
        # データ自体はちゃんと格納されている
        worker.tasks.add(task)
        return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
    return render(request, "shift/specification.html", {
        "task": task, 
        "member_num": len(task.workers.all()), 
        "worker": worker, 
        "tasks_of_worker": worker.tasks.all(),
        "now": now
    })

@login_checker
def confirm(request):
    worker = Worker.objects.get(id=request.session["worker_id"])
    tasks = worker.tasks.all()
    return render(request, "shift/confirm.html", {
        "tasks": tasks, 
        "now": now
    })

@login_checker
def make(request):
    return HttpResponse("make")

@login_checker
def revise(request):
    return HttpResponse("revise")

@login_checker
def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data["text"]
            print(input_text)
            feedback = Feedback(text=input_text, response="", date=now)
            feedback.save()
            return HttpResponseRedirect(reverse("shift:feedback"))
    
    feedbacks = Feedback.objects.all()
    return render(request, "shift/feedback.html", {
        "form": FeedbackForm(), 
        "feedbacks": feedbacks, 
        "now": now
    })