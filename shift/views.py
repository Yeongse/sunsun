from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from tabnanny import check
from django.contrib.auth.hashers import make_password, check_password

from .models import Task, Worker, Feedback
from .forms import LoginForm



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
                    return HttpResponseRedirect(reverse("shift:home"))
                else:
                    err_message = "パスワードが正しくありません"            
       
    return render(request, "shift/login.html", {
        "message": err_message, 
        "form": LoginForm()
    })


def home(request):
    worker = Worker.objects.get(id=request.session["worker_id"])
    return HttpResponse(worker.name)
    


def specification(request):
    return 0


def make(request):
    return 0


def revise(request):
    return 0


def feedback(request):
    return 0