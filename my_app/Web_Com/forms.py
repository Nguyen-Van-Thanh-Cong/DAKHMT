from django import forms
# from django.contrib.auth.models import User
from .models import *  

class DangKyForm(forms.Form):
    ten_kh = forms.CharField(label='Họ tên')
    sdt = forms.CharField(label='Số điện thoại')
    dia_chi = forms.CharField(label='Địa chỉ')
    email = forms.EmailField(label='Email')
    
    ten_dn = forms.CharField(label='Tên đăng nhập')
    mk = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)


class DangNhapForm(forms.Form):
    ten_dn = forms.CharField(label="Tên đăng nhập")
    mk = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")


class LienHeForm(forms.ModelForm):
    class Meta:
        model = LienHe
        fields = ['nd_lh']
        labels = {'nd_lh': "Nội dung liên hệ"}
