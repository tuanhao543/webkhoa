from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # trang chu
    path('', views.home, name='home'),
    
    # giang vien
    path('login_gv/', views.login_GV, name='login_gv'),
    path('giang_vien/<msgv>/', views.trang_giang_vien, name='trang_giang_vien'),
    path('thong_tin_gv/<msgv>/', views.thongtin_GV, name='thongtin_GV'),
    path('xem_lich_day_gv/<str:msgv>/', views.xem_lich_day_gv, name='xem_lich_day_gv'),
    
    
    path('chon_mon/<str:msgv>/', views.trang_chon_mon, name='trang_chon_mon'),
    path('lop_hoc/<str:ma_mon>/<str:msgv>/', views.trang_lop_hoc, name='trang_lop_hoc'),
    path('xem-diem/<slug:slug_lop>/<str:msgv>/', views.xem_diem_giang_vien, name='xem_diem_giang_vien'),
    # sinh viên
    path('login_sv/', views.login_SV, name='login_sv'),
    path('sinh_vien/<mssv>/', views.trang_sinh_vien, name='trang_sinh_vien'),
    path('thong_tin_sv/<mssv>/', views.thongtin_SV, name='thongtin_SV'),
    path('xem_diem/<mssv>/', views.xem_diem_sinh_vien, name='xem_diem_sinh_vien'),
    path('xem_lich_hoc_sv/<str:mssv>/', views.xem_lich_hoc_sv, name='xem_lich_hoc_sv'),
]