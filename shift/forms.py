from django import forms
from pkg_resources import require
from .models import *

class LoginForm(forms.Form):
    name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
    password = forms.CharField(label="パスワード", widget=forms.TextInput(attrs={"placeholder": "Password"}))

class FeedbackForm(forms.Form):
    text = forms.CharField(label="内容", widget=forms.Textarea())

class PersonalForm(forms.Form):
    name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
    password1 = forms.CharField(label="パスワード", widget=forms.TextInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(label="パスワードをもう一度", widget=forms.TextInput(attrs={"placeholder": "Password"}))
    email = forms.CharField(label="メールアドレス", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))

class RegisterForm(forms.Form):
    name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
    email = forms.CharField(label="メールアドレス", widget=forms.TextInput(attrs={"placeholder": "メールアドレス"}))
    is_admin = forms.BooleanField()

class ReviseForm(forms.Form):
    name = forms.CharField(label="名前")
    date = forms.DateField(label="日付")
    startTime = forms.CharField(label="開始時刻", widget=forms.TextInput(attrs={"placeholder": "XX:YY"}))
    endTime = forms.CharField(label="終了時刻", widget=forms.TextInput(attrs={"placeholder": "XX:YY"}))
    specification = forms.CharField(label="詳細内容", widget=forms.Textarea())
    type = forms.ChoiceField(label="業務種別", choices=(("CL外業務", "CL外業務"), ("CL業務", "CL業務"), ("その他", "その他")))
    capacity = forms.IntegerField(label="募集人数")
    extra = forms.CharField(label="特筆事項", widget=forms.Textarea())

class ReassignForm(forms.Form):
    add = forms.ModelChoiceField(label="出勤者の追加", required=False, queryset=Worker.objects.none())
    remove = forms.ModelChoiceField(label="出勤者の削除", required=False, queryset=Worker.objects.none())

class MakeForm(forms.Form):
    name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
    password = forms.CharField(label="パスワード", widget=forms.TextInput(attrs={"placeholder": "Password"}))