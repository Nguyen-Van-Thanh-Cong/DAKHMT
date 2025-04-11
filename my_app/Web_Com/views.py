from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'home.html')

def sanpham(request):
    sanphams = SanPham.objects.all()
    return render(request, 'sanpham.html', {'sanphams': sanphams})

def chitiet(request, id_sp):
    sanpham = get_object_or_404(SanPham, id_sp=id_sp)
    return render(request, 'chitiet.html', {'sanpham': sanpham})

def dang_ky(request):
    if request.method == 'POST':
        form = DangKyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công. Mời đăng nhập.")
            return redirect('dang_nhap')
    else:
        form = DangKyForm()
    return render(request, 'dangky.html', {'form': form})


def dang_nhap(request):
    if request.method == 'POST':
        form = DangNhapForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base')  
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        form = DangNhapForm()
    return render(request, 'login.html', {'form': form})


def dang_xuat(request):
    logout(request)
    return redirect('base')


def lienhe(request):
    if request.method == 'POST':
        form = LienHeForm(request.POST)
        if form.is_valid():
            lh = form.save(commit=False)
            if request.user.is_authenticated:
                lh.id_kh = request.user.id  
            lh.save()
            messages.success(request, "Cảm ơn bạn đã liên hệ.")
            return redirect('base')
    else:
        form = LienHeForm()
    return render(request, 'lienhe.html', {'form': form})