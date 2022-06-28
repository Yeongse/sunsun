from django.urls import path

from . import views

app_name = "shift"

urlpatterns = [
    path("login", views.login, name="login"), 
    path("home/<int:year>/<int:month>", views.home, name="home"), 
    path("specification/<int:task_id>", views.specification, name="specification"), 
    path("confirm", views.confirm, name="confirm"), 
    path("personal", views.personal, name="personal"), 
    path("make/<int:past_task_id>", views.make, name="make"), 
    path("recall", views.recall, name="recall"), 
    path("revise/<int:task_id>", views.revise, name="revise"), 
    path("reassign/<int:task_id>", views.reassign, name="reassign"), 
    path("register", views.register, name="register"),
    path("delete", views.delete, name="delete"), 
    path("instruction", views.instruction, name="instruction"),  
    path("feedback", views.feedback, name="feedback"), 
    path("logout", views.logout, name="logout")
]