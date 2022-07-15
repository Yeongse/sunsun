from asyncio import tasks
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages

from .models import Task, Worker, Feedback
from .forms import LoginForm, InitializeForm, FeedbackForm, PersonalForm, RegisterForm, DeleteForm, ReviseForm, ReassignForm, MakeForm, RecallForm


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

    if request.method ==  "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            input_name = form.cleaned_data["name"]
            input_password = form.cleaned_data["password"]
            matched_workers = Worker.objects.filter(name=input_name)

            # ユーザ名の確認
            if len(matched_workers) == 0:
                messages.error(request, "ユーザ名が正しくありません")
            else:
                worker = matched_workers[0]
                is_auth = check_password(input_password, worker.password)

                # パスワードの確認
                if is_auth:
                    request.session["worker_id"] = worker.id
                    # 初期パスワードの場合に変更を強制
                    if input_password == "0000":
                        return HttpResponseRedirect(reverse("shift:initialize"))
                    else:
                        messages.success(request, f"お疲れ様です、{worker.name}様")
                        return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
                else:
                    messages.error(request, "パスワードが正しくありません")         
    

    return render(request, "shift/login.html", {
        "form": LoginForm()
    })

@login_checker
def initialize(request):
    message = ""
    worker = Worker.objects.get(id=request.session["worker_id"])

    if request.method == "POST":
        form = InitializeForm(request.POST)
        if form.is_valid():
            input_password1 = form.cleaned_data["password1"]
            input_password2 = form.cleaned_data["password2"]

            # 2回入力のパスワードが合っているかの確認
            if input_password1 == input_password2:
                # 変更なしを許さない
                if input_password1 == "0000":
                    message = "パスワードを変更してください"
                else:
                    worker.password = make_password(input_password1)
                    worker.save()
                return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
            else:
                message = "パスワードが一致していません"

    return render(request, "shift/initialize.html", {
        "message": message, 
        "form": InitializeForm()
    })

@login_checker
def index(request):
    return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
    
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

        mail_subject = "申し込み完了の通知"
        mail_context = {
            "task": task, 
            "worker": worker
        }
        mail_message_html = render_to_string("shift/mails/apply_notice.html", mail_context, request)
        mail_message = strip_tags(mail_message_html)
        mail_from_email = settings.DEFAULT_FROM_EMAIL
        mail_recipient_list = [worker.email]
        send_mail(subject=mail_subject, message=mail_message, from_email=mail_from_email, recipient_list=mail_recipient_list)

        messages.success(request, "業務への応募が完了しました")
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
                messages.success(request, "登録情報が変更されました")
                return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
            else:
                messages.error(request, "パスワードが一致していません")
    
    initial_value = {
        "name": worker.name, 
        "password1": "", 
        "password2": "", 
        "email": worker.email
    }
    
    return render(request, "shift/personal.html", {
        "worker": worker, 
        "form": PersonalForm(initial=initial_value)
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

            non_admin_workers = Worker.objects.exclude(is_admin=True).all()
            mail_subject = "募集開始の通知"
            mail_context = {
                "task": task
            }
            mail_message_html = render_to_string("shift/mails/made_notice.html", mail_context, request)
            mail_message = strip_tags(mail_message_html)
            mail_bcc_list = [worker.email for worker in non_admin_workers]
            mail = EmailMessage(
                subject=mail_subject, 
                body=mail_message, 
                from_email = settings.DEFAULT_FROM_EMAIL, 
                to=[settings.DEFAULT_FROM_EMAIL], 
                bcc=mail_bcc_list
                )
            mail.send()

            messages.success(request, "業務が作成されました")
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

            messages.success(request, "業務が修正されました")
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
        "task": task, 
        "form": ReviseForm(initial_value)
    })

@login_checker
def reassign(request, task_id):
    comment = ""
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        form = ReassignForm(request.POST)
        if form.is_valid():
            added_worker = form.cleaned_data["add"]
            removed_worker = form.cleaned_data["remove"]

            if added_worker != None:
                added_worker.tasks.add(task)
            if removed_worker != None:
                removed_worker.tasks.remove(task)
            messages.success(request, "勤務者が変更されました")
            return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))

    assigned_worker = task.workers.all()
    non_assigned_worker = Worker.objects.exclude(tasks=task).all()
    if len(task.workers.all()) >= task.capacity:
        comment = "定員のため、勤務者の追加はできません"
        non_assigned_worker = Worker.objects.none()
    
    form = ReassignForm()
    form.fields["add"].queryset = non_assigned_worker
    form.fields["remove"].queryset = assigned_worker

    return render(request, "shift/reassign.html", {
        "comment": comment,
        "task": task, 
        "form": form
    })

@login_checker
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            input_name = form.cleaned_data["name"]
            input_email = form.cleaned_data["email"]
            input_is_admin = form.cleaned_data["is_admin"]

            if len(Worker.objects.filter(email=input_email)) > 0:
                messages.error(request, "そのユーザは既に登録されています")
            else:
                worker = Worker(name=input_name, email=input_email, password=make_password("0000"), is_admin=input_is_admin)
                worker.save()
                messages.success(request, "従業員が登録されました")
                return HttpResponseRedirect(reverse("shift:register"))
            
    return render(request, "shift/register.html", {
        "form": RegisterForm()
    })

@login_checker
def delete(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            delete_worker = form.cleaned_data["delete"]
            assigned_task = delete_worker.tasks.all()
            future_task = assigned_task.filter(date__gt=now)

            if len(future_task) > 0:
                messages.error(request, "勤務予定の業務があるので削除できませんでした")
            else:
                delete_worker.delete()
                messages.success(request, "従業員が削除されました")
                return HttpResponseRedirect(reverse("shift:home", args=[now.year, now.month]))
    
    form = DeleteForm()
    form.fields["delete"].queryset = Worker.objects.exclude(id=request.session["worker_id"]).all()

    return render(request, "shift/delete.html", {
        "form": form
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
            messages.success(request, "フィードバックが送信されました")
            return HttpResponseRedirect(reverse("shift:feedback"))
    
    feedbacks = Feedback.objects.all()
    return render(request, "shift/feedback.html", {
        "form": FeedbackForm(), 
        "feedbacks": feedbacks
    })

@login_checker
def logout(request):
    del request.session["worker_id"]
    messages.success(request, "ログアウトが完了しました")
    return HttpResponseRedirect(reverse("shift:login"))

def remind(request):
    tomorrow = now+datetime.timedelta(days=1)
    tasks = Task.objects.filter(date=tomorrow)
    for task in tasks:
        workers = task.workers.all()
        for worker in workers:
            mail_subject = "出勤前日のリマインド"
            mail_context = {
                "task": task, 
                "worker": worker
            }
            mail_message_html = render_to_string("shift/mails/remind_notice.html", mail_context, request)
            mail_message = strip_tags(mail_message_html)
            mail_from_email = settings.DEFAULT_FROM_EMAIL
            mail_recipient_list = [worker.email]
            send_mail(subject=mail_subject, message=mail_message, from_email=mail_from_email, recipient_list=mail_recipient_list)
    return HttpResponse("reminder mail sended")

def urge(request):
    two_days_after_tomorrow = now+datetime.timedelta(days=3)
    tasks = Task.objects.filter(date=two_days_after_tomorrow)
    for task in tasks:
        if len(task.workers.all()) < task.capacity:
            non_admin_workers = Worker.objects.exclude(is_admin=True).all()
            mail_subject = "人員不足の業務に関する催促"
            mail_context = {
                "task": task
            }
            mail_message_html = render_to_string("shift/mails/urge_notice.html", mail_context, request)
            mail_message = strip_tags(mail_message_html)
            mail_bcc_list = [worker.email for worker in non_admin_workers]
            mail = EmailMessage(
                subject=mail_subject, 
                body=mail_message, 
                from_email = settings.DEFAULT_FROM_EMAIL, 
                to=[settings.DEFAULT_FROM_EMAIL], 
                bcc=mail_bcc_list
                )
            mail.send()
    return HttpResponse("reminder mail sended")