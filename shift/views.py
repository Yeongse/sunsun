from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

from .models import Task, Worker, Feedback
from .forms import LoginForm, FeedbackForm, PersonalForm, RegisterForm, ReviseForm, ReassignForm, MakeForm, RecallForm


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
    message = ""
    if request.method ==  "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            input_name = form.cleaned_data["name"]
            input_password = form.cleaned_data["password"]
            matched_workers = Worker.objects.filter(name=input_name)

            # check username
            if len(matched_workers) == 0:
                message = "ユーザ名が正しくありません"
            else:
                worker = matched_workers[0]
                is_auth = check_password(input_password, worker.password)

                # check password
                if is_auth:
                    request.session["worker_id"] = worker.id
                    return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
                else:
                    message = "パスワードが正しくありません"            
    

    return render(request, "shift/login.html", {
        "message": message, 
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

            # 業務とそこで今のところ配属された人数をまとめて辞書で保存して渡す
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
        worker.tasks.add(task)
        return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
    
    return render(request, "shift/specification.html", {
        "task": task, 
        "member_num": len(task.workers.all()), 
        "worker": worker, 
        "workers_of_task": task.workers.all(), 
        "tasks_of_worker": worker.tasks.all()
    })

@login_checker
def confirm(request):
    worker = Worker.objects.get(id=request.session["worker_id"])
    tasks = worker.tasks.all()

    return render(request, "shift/confirm.html", {
        "tasks": tasks
    })

@login_checker
def personal(request):
    worker = Worker.objects.get(id=request.session["worker_id"])
    message = ""
    
    if request.method == "POST":
        form = PersonalForm(request.POST)
        if form.is_valid():
            input_name = form.cleaned_data["name"]
            input_password1 = form.cleaned_data["password1"]
            input_password2 = form.cleaned_data["password2"]
            input_email = form.cleaned_data["email"]

            # 2回入力のパスワードが合っているかの確認
            if input_password1 == input_password2:
                worker.name = input_name
                worker.password = make_password(input_password1)
                worker.email = input_email
                worker.save()
                return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
            else:
                message = "パスワードが一致していません"
    
    initial_value = {
        "name": worker.name, 
        "password1": "", 
        "password2": "", 
        "email": worker.email
    }
    
    return render(request, "shift/personal.html", {
        "worker": worker, 
        "form": PersonalForm(initial=initial_value), 
        "message": message
    })

@login_checker
def make(request, past_task_id):
    if request.method == "POST":
        form = MakeForm(request.POST)
        if form.is_valid():
            input_name = form.cleaned_data["name"]
            input_date = form.cleaned_data["date"]
            input_startTime = form.cleaned_data["startTime"]
            input_endTime = form.cleaned_data["endTime"]
            input_specification = form.cleaned_data["specification"]
            input_type = form.cleaned_data["type"]
            input_capacity = form.cleaned_data["capacity"]
            input_extra = form.cleaned_data["extra"]

            task = Task(
                name=input_name, 
                date=input_date, 
                startTime=input_startTime, 
                endTime=input_endTime, 
                specification=input_specification, 
                type=input_type, 
                capacity=input_capacity, 
                extra=input_extra
                )
            task.save()
            return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))

    initial_value = {}
    # 初期値0以外のpast_task_idが渡された場合, formの初期値を設定する
    if past_task_id != 0:
        past_task = Task.objects.get(id=past_task_id)
        initial_value = {
            "name": past_task.name, 
            "specification": past_task.specification, 
            "date": past_task.date, 
            "startTime": past_task.startTime, 
            "endTime": past_task.endTime, 
            "type": past_task.type, 
            "capacity": past_task.capacity, 
            "extra": past_task.extra
        }
    
    return render(request, "shift/make.html", {
        "recall_form": RecallForm(), 
        "make_form": MakeForm(initial=initial_value)
    })

@login_checker
def recall(request):
    if request.method == "POST":
        form = RecallForm(request.POST)
        if form.is_valid():
            past_task = form.cleaned_data["pastTask"]
            return HttpResponseRedirect(reverse("shift:make", args=[past_task.id]))

@login_checker
def revise(request, task_id):
    message = ""
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        form = ReviseForm(request.POST)

        if form.is_valid():
            input_name = form.cleaned_data["name"]
            input_date = form.cleaned_data["date"]
            input_startTime = form.cleaned_data["startTime"]
            input_endTime = form.cleaned_data["endTime"]
            input_specification = form.cleaned_data["specification"]
            input_type = form.cleaned_data["type"]
            input_capacity = form.cleaned_data["capacity"]
            input_extra = form.cleaned_data["extra"]

            task.name = input_name
            task.date = input_date
            task.startTime = input_startTime
            task.endTime = input_endTime
            task.specification = input_specification
            task.type = input_type
            task.capacity = input_capacity
            task.extra = input_extra
            task.save()

            return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))


    initial_value = {
        "name": task.name, 
        "date": task.date, 
        "startTime": task.startTime, 
        "endTime": task.endTime, 
        "specification": task.specification, 
        "type": task.type, 
        "capacity": task.capacity, 
        "extra": task.extra
    }
    return render(request, "shift/revise.html", {
        "message": message, 
        "task": task, 
        "form": ReviseForm(initial_value)
    })

@login_checker
def reassign(request, task_id):
    message = ""
    task = Task.objects.get(id = task_id)
    

    if request.method == "POST":
        form = ReassignForm(request.POST)
        if form.is_valid():
            added_worker = form.cleaned_data["add"]
            removed_worker = form.cleaned_data["remove"]

            if added_worker != None:
                added_worker.tasks.add(task)
            if removed_worker != None:
                removed_worker.tasks.remove(task)
            return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))

    assigned_worker = task.workers.all()
    non_assigned_worker = Worker.objects.exclude(tasks=task).all()
    if len(task.workers.all()) >= task.capacity:
        message = "定員のため、勤務者の追加はできません"
        non_assigned_worker = Worker.objects.none()
    
    form = ReassignForm()
    form.fields["add"].queryset = non_assigned_worker
    form.fields["remove"].queryset = assigned_worker

    return render(request, "shift/reassign.html", {
        "message": message,
        "task": task, 
        "form": form
    })

@login_checker
def register(request):
    message = ""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            input_name = form.cleaned_data["name"]
            input_email = form.cleaned_data["email"]
            input_is_admin = form.cleaned_data["is_admin"]

            if len(Worker.objects.filter(email=input_email)) > 0:
                message = "そのユーザは既に登録されています"
            else:
                worker = Worker(name=input_name, email=input_email, password=make_password("0000"), is_admin=input_is_admin)
                worker.save()
                return HttpResponseRedirect(reverse("shift:register"))
            
    return render(request, "shift/register.html", {
        "form": RegisterForm(), 
        "message": message
    })

@login_checker
def instruction(request):
    return render(request, "shift/instruction.html", {})

@login_checker
def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data["text"]
            feedback = Feedback(text=input_text, response="", date=now)
            feedback.save()
            return HttpResponseRedirect(reverse("shift:feedback"))
    
    feedbacks = Feedback.objects.all()
    return render(request, "shift/feedback.html", {
        "form": FeedbackForm(), 
        "feedbacks": feedbacks
    })