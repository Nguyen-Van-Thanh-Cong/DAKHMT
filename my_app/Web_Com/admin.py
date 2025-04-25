from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = "Quản trị Cửa hàng Cốm Mễ Trì"
admin.site.site_title = "Trang quản trị cốm"
admin.site.index_title = "Chào mừng đến với trang quản trị"
admin.site.register(SanPham)
admin.site.register(KhachHang)
admin.site.register(TaiKhoan)
admin.site.register(DonHang)
admin.site.register(ChiTietDonHang)
admin.site.register(LienHe)
