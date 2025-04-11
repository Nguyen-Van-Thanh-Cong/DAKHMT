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
    path('lien-he/', views.lienhe, name='lienhe'),
]