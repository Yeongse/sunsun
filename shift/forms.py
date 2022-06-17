from django import forms

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
    name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
    password = forms.CharField(label="パスワード", widget=forms.TextInput(attrs={"placeholder": "Password"}))

class MakeForm(forms.Form):
    name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
    password = forms.CharField(label="パスワード", widget=forms.TextInput(attrs={"placeholder": "Password"}))