from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label="ユーザ名")
    password = forms.CharField(label="パスワード")