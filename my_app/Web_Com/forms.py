from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *  

class DangKyForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DangNhapForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập")
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")


class LienHeForm(forms.ModelForm):
    class Meta:
        model = LienHe
        fields = ['nd_lh']
        labels = {'nd_lh': "Nội dung liên hệ"}
