import datetime
from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
            khach_hang = KhachHang.objects.create(
                ten_kh=form.cleaned_data['ten_kh'],
                sdt=form.cleaned_data['sdt'],
                dia_chi=form.cleaned_data['dia_chi'],
                email=form.cleaned_data['email']
            )

            TaiKhoan.objects.create(
                id_kh=khach_hang,
                ten_dn=form.cleaned_data['ten_dn'],
                mk=form.cleaned_data['mk']  
            )

            return redirect('Web_Com:login')
    else:
        form = DangKyForm()
    return render(request, 'dangky.html', {'form': form})


def dang_nhap(request):
    if request.method == 'POST':
        ten_dn = request.POST.get('ten_dn')
        mk = request.POST.get('mk')

        try:
            tk = TaiKhoan.objects.get(ten_dn=ten_dn, mk=mk)
            request.session['id_kh'] = tk.id_kh.id_kh
            request.session['ten_kh'] = tk.id_kh.ten_kh
            return redirect('Web_Com:home')  
        except TaiKhoan.DoesNotExist:
            messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu.')

    return render(request, 'login.html')


def dang_xuat(request):
    request.session.flush()
    return redirect('Web_Com:home')


def thong_tin_ca_nhan(request):
    id_kh = request.session.get('id_kh')
    if not id_kh:
        return redirect('Web_Com:login')

    kh = KhachHang.objects.get(id_kh=id_kh)

    if request.method == 'POST':
        kh.ten_kh = request.POST.get('ten_kh')
        kh.sdt = request.POST.get('sdt')
        kh.dia_chi = request.POST.get('dia_chi')
        kh.email = request.POST.get('email')
        kh.save()
        messages.success(request, "Cập nhật thông tin thành công!")

    return render(request, 'thongtin.html', {'kh': kh})

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

def them_vao_gio(request, id_sp):
    id_kh = request.session.get('id_kh')
    if not id_kh:
        return redirect('Web_Com:login')

    san_pham = get_object_or_404(SanPham, id_sp=id_sp)

    don_hang, created = DonHang.objects.get_or_create(
        id_kh_id=id_kh,
        trang_thai='Giỏ hàng'
    )

    chi_tiet, created = ChiTietDonHang.objects.get_or_create(
        id_dh=don_hang,
        id_kh_id=id_kh,
        id_sp=san_pham,
        defaults={'so_luong': 1, 'gia': san_pham.gia}
    )

    if not created:
        chi_tiet.so_luong += 1
        chi_tiet.save()

    if request.GET.get('redirect') == 'giohang':
        return redirect('Web_Com:giohang')

    
    return redirect('Web_Com:chitiet', id_sp=id_sp)

def gio_hang(request):
    id_kh = request.session.get('id_kh')
    
    if not id_kh:
        return redirect('Web_Com:login')  
    try:
        don_hang = DonHang.objects.get(id_kh=id_kh, trang_thai='Giỏ hàng')
        chi_tiet = ChiTietDonHang.objects.filter(id_dh=don_hang)
        
        tong_sp = sum(item.so_luong for item in chi_tiet)
        tong_tien = sum(item.so_luong * item.gia for item in chi_tiet)

        don_hang.tong_sp = tong_sp
        don_hang.tong_tien = tong_tien
        don_hang.save()

        for item in chi_tiet:
            item.tong_tien = item.so_luong * item.gia
    except DonHang.DoesNotExist:
        don_hang = None
        chi_tiet = []

    return render(request, 'giohang.html', {'don_hang': don_hang, 'chi_tiet': chi_tiet})

def cap_nhat_so_luong(request, id_sp):
    if request.method == 'POST':
        id_kh = request.session.get('id_kh')
        if not id_kh:
            return redirect('Web_Com:login')

        so_luong = int(request.POST.get('so_luong'))
        don_hang = DonHang.objects.get(id_kh_id=id_kh, trang_thai='Giỏ hàng')
        ct = ChiTietDonHang.objects.get(id_dh=don_hang, id_sp__id_sp=id_sp)
        ct.so_luong = so_luong
        ct.save()

        don_hang.tong_sp = sum(item.so_luong for item in ChiTietDonHang.objects.filter(id_dh=don_hang))
        don_hang.tong_tien = sum(item.so_luong * item.gia for item in ChiTietDonHang.objects.filter(id_dh=don_hang))
        don_hang.save()

    return redirect('Web_Com:giohang')

def xoa_san_pham_gio(request, id_sp):
    id_kh = request.session.get('id_kh')
    if not id_kh:
        return redirect('Web_Com:login')

    try:
        don_hang = DonHang.objects.get(id_kh_id=id_kh, trang_thai='Giỏ hàng')
        ChiTietDonHang.objects.filter(id_dh=don_hang, id_sp__id_sp=id_sp).delete()
    except DonHang.DoesNotExist:
        pass

    return redirect('Web_Com:giohang')

def dat_hang(request):
    id_kh = request.session.get('id_kh')
    if not id_kh:
        return redirect('Web_Com:login')

    don_hang = DonHang.objects.get(id_kh_id=id_kh, trang_thai='Giỏ hàng')
    don_hang.trang_thai = 'Đã đặt hàng'
    don_hang.ngay_dat = datetime.now()
    don_hang.save()

    return redirect('Web_Com:lichsu')

def lich_su_don_hang(request):
    id_kh = request.session.get('id_kh')

    if not id_kh:
        return redirect('Web_Com:login')  

    don_hangs = DonHang.objects.filter(id_kh=id_kh).exclude(trang_thai='Giỏ hàng').order_by('-ngay_dat')
    return render(request, 'lichsu.html', {'don_hangs': don_hangs})

def chi_tiet_don_hang(request, id_dh):
    id_kh = request.session.get('id_kh')
    if not id_kh:
        return redirect('Web_Com:login')

    don_hang = get_object_or_404(DonHang, id_dh=id_dh, id_kh_id=id_kh)
    chi_tiet = ChiTietDonHang.objects.filter(id_hd=don_hang)
    return render(request, 'chitiet.html', {'don_hang': don_hang, 'chi_tiet': chi_tiet})