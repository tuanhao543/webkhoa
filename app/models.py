from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.


# Bảng Monhoc
class Monhoc(models.Model):
    ma_mon = models.CharField(max_length=20, primary_key=True)
    ten_mon = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.ten_mon

# lop
class Lophoc(models.Model):
    ma_lop = models.CharField(max_length=20, primary_key=True)
    ten_lop = models.CharField(max_length=50, null=True)
    slug_lop = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.ten_lop

    
# bang Sinhvien
class Sinhvien(models.Model):
    mssv = models.CharField(primary_key=True, max_length=20)
    password_sv = models.CharField(max_length=20, null=True, blank=False)
    hovaten_sv = models.CharField(max_length=30, null=True, blank=False)
    hoclop = models.ForeignKey(Lophoc, on_delete=models.SET_NULL, null=True, related_name='sinh_vien')
    namsinh_sv = models.DateField()
    gioitinh_sv = models.CharField(max_length=30, null=True, blank=False)
    diachi_sv = models.CharField(max_length=200, null=True, blank=False)
    noisinh_sv = models.CharField(max_length=50, null=True, blank=False)
    quequan_sv = models.CharField(max_length=50, null=True, blank=False)
    image_sv = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.hovaten_sv
    
       

class Giangvien(models.Model):
    msgv = models.CharField(primary_key=True, max_length=20)
    password_gv = models.CharField(max_length=20, null=True, blank=False)
    hovaten_gv = models.CharField(max_length=30, null=True, blank=False)
    namsinh_gv = models.DateField()
    gioitinh_gv = models.CharField(max_length=30, null=True, blank=False)
    diachi_gv = models.CharField(max_length=200, null=True, blank=False)
    noisinh_gv = models.CharField(max_length=50, null=True, blank=False)
    quequan_gv = models.CharField(max_length=50, null=True, blank=False)
    image_gv = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.hovaten_gv


    

# Bảng Diem cập nhật cho phép Giảng viên liên quan đến việc nhập điểm
class Bangdiem(models.Model):
    sinhvien = models.ForeignKey(Sinhvien, on_delete=models.CASCADE)
    lop = models.ForeignKey(Lophoc, on_delete=models.CASCADE, null=True)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE)
    giang_vien = models.ForeignKey(Giangvien, on_delete=models.CASCADE)
    diem_giua_ky = models.FloatField(null=True, blank=True)
    diem_cuoi_ky = models.FloatField(null=True, blank=True)
    diem_tong_ket = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.diem_giua_ky is not None and self.diem_cuoi_ky is not None:
            self.diem_tong_ket = (0.4*self.diem_giua_ky) + (0.6*self.diem_cuoi_ky)
        super(Bangdiem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.sinhvien.mssv} - {self.monhoc.ten_mon} - {self.diem_tong_ket}'

# Bảng Thoikhoabieu cập nhật cho phép xác định các môn học của từng Sinhvien và các môn Giangvien dạy
class Lichhoc(models.Model):
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE, related_name='mon_hoctkb')
    lophocmon = models.ForeignKey(Lophoc, on_delete=models.CASCADE, related_name='lop_hoctkb')
    giang_vien = models.ForeignKey(Giangvien, on_delete=models.CASCADE, related_name='giang_vientkb')
    ca_hoc = models.IntegerField()
    ngay_bat_dau = models.DateField()
    ngay_ket_thuc = models.DateField()
    ngay_trong_tuan = models.IntegerField()

    def __str__(self):
        return f'{self.monhoc.ten_mon} - {self.lophocmon.ten_lop} - {self.giang_vien.hovaten_gv} - Ca {self.ca_hoc} - {self.ngay_bat_dau} - {self.ngay_ket_thuc} - Thứ {self.ngay_trong_tuan}'
