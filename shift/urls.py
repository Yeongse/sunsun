from django.urls import path

from . import views

app_name = "shift"

urlpatterns = [
    path("", views.index, name="index"), 
    path("login", views.login, name="login"), 
    path("home", views.home, name="home"), 
    path("specification/<int:task_id>", views.specification, name="specification"), 
    path("make", views.make, name="make"), 
    path("revise/<int:task_id>", views.revise, name="revise"), 
    path("feedback", views.feedback, name="feedback")
]