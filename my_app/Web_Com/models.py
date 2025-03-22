from django.db import models

# Create your models here.
# Bảng sản phẩm
class SanPham(models.Model):
    id_sp = models.AutoField(primary_key=True)
    ten_sp = models.CharField(max_length=100, null=False)
    gia = models.IntegerField(null=False)
    mo_ta = models.TextField(null=False)
    hinh_anh = models.ImageField(upload_to='static/images/', null=True, blank=True)

    def __str__(self):
        return self.ten_sp

# Bảng khách hàng
class KhachHang(models.Model):
    id_kh = models.AutoField(primary_key=True)
    ten_kh = models.CharField(max_length=50, null=False)
    sdt = models.CharField(max_length=10, null=False, unique=True)
    dia_chi = models.TextField(null=False)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.ten_kh

# Bảng tài khoản
class TaiKhoan(models.Model):
    id_tk = models.AutoField(primary_key=True)
    khach_hang = models.OneToOneField(KhachHang, on_delete=models.CASCADE)
    ten_dn = models.CharField(max_length=50, unique=True, null=False)
    mk = models.CharField(max_length=128, null=False)  

    def __str__(self):
        return self.ten_dn

# Bảng đơn hàng
class DonHang(models.Model):
    TRANG_THAI_CHOICES = [
        ('DA_DAT', 'Đã đặt hàng'),
        ('XAC_NHAN', 'Đã xác nhận và chuẩn bị vận chuyển'),
        ('DANG_VC', 'Đang vận chuyển'),
        ('THANH_CONG', 'Nhận hàng và thanh toán thành công'),
        ('HUY', 'Hủy đơn hàng'),
    ]

    id_dh = models.AutoField(primary_key=True)
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    tong_sp = models.IntegerField(default=0)
    tong_tien = models.IntegerField(default=0)
    ngay_dat = models.DateTimeField(auto_now_add=True)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='DA_DAT')

    def __str__(self):
        return f"Đơn hàng {self.id_dh} - {self.khach_hang.ten_kh}"

# Bảng chi tiết đơn hàng
class ChiTietDonHang(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE)
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    so_luong = models.IntegerField(null=False)
    gia = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.san_pham.ten_sp} - SL: {self.so_luong}"

# Bảng liên hệ
class LienHe(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    nd_lh = models.TextField(null=False)
    ngay_lh = models.DateTimeField(auto_now_add=True)
    phan_hoi = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Liên hệ từ {self.khach_hang.ten_kh} ngày {self.ngay_lh}"