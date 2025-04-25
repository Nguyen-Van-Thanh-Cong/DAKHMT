from django.urls import path
from . import views

app_name = 'Web_Com'
urlpatterns = [
    path('', views.home, name='home'),
    path('sanpham/', views.sanpham, name='sanpham'),
    path('sanpham/<int:id_sp>/', views.chitiet, name='chitiet'),
    path('dang-ky/', views.dang_ky, name='dang_ky'),
    path('dang-nhap/', views.dang_nhap, name='login'),
    path('dang-xuat/', views.dang_xuat, name='dang_xuat'),
    path('thong-tin/', views.thong_tin_ca_nhan, name='thong_tin_ca_nhan'),
    path('lien-he/', views.lienhe, name='lienhe'),
    path('giohang/them/<int:id_sp>/', views.them_vao_gio, name='them_vao_gio'),
    path('giohang/', views.gio_hang, name='giohang'),
    path('giohang/cap-nhat/<int:id_sp>/', views.cap_nhat_so_luong, name='cap_nhat_so_luong'),
    path('giohang/xoa/<int:id_sp>/', views.xoa_san_pham_gio, name='xoa_san_pham_gio'),
    path('dathang/', views.dat_hang, name='dathang'),
    path('lich-su-don-hang/', views.lich_su_don_hang, name='lichsu'),
    path('don-hang/<int:id_dh>/', views.chi_tiet_don_hang, name='chi_tiet_don'),
]