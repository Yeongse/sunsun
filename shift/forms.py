from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
    password = forms.CharField(label="パスワード", widget=forms.TextInput(attrs={"placeholder": "Password"}))

class FeedbackForm(forms.Form):
    text = forms.CharField(label="内容", widget=forms.Textarea())