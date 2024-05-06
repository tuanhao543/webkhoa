from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import transaction
from django.forms import modelformset_factory
from django.forms import formset_factory


# Create your views here.
def home(request):
    return render(request, 'app/home.html',)


# Giảng Viên
# Đăng nhập Giảng Viên
def login_GV(request):
    if request.method == "POST":
        msgv = request.POST.get('msgv')
        password_gv = request.POST.get('password_gv')
        giangvien = Giangvien.objects.filter(msgv=msgv).first()
        if giangvien and giangvien.password_gv == password_gv:
        # Đăng nhập thành công
            request.session['giangvien_id'] = giangvien.msgv
            giang_vien_url = reverse('trang_giang_vien', kwargs={'msgv': giangvien.msgv})
            return redirect(giang_vien_url)
        else:
            messages.info(request, 'MSGV hoặc Mật Khẩu không đúng!')
    return render(request, 'app/dang_nhap_cua_giang_vien.html') 


def thongtin_GV(request, msgv):
    # Lấy thông tin sinh viên dựa vào 'mssv' từ session
    msgv = request.session.get('giangvien_id')
    giangvien = Giangvien.objects.get(msgv=msgv)
    # Truyền dữ liệu cần thiết về template
    context = {'giangvien': giangvien}
    return render(request, 'app/thong_tin_giang_vien.html', context)


def trang_giang_vien(request, msgv):
    # Đảm bảo rằng chỉ giảng viên đã đăng nhập mới có thể truy cập trang này
    if 'giangvien_id' not in request.session:
        # Chưa đăng nhập, chuyển hướng về trang đăng nhập
        return redirect('login_GV')
    # Lấy thông tin giảng viên dựa vào MSGV lưu trong session
    msgv = request.session.get('giangvien_id')
    giangvien = Giangvien.objects.get(msgv=msgv)
    # Truyền dữ liệu cần thiết về template
    context = {
        'giangvien': giangvien,
    }
    return render(request, 'app/trang_giang_vien.html', context)


def xem_lich_day_gv(request, msgv):
    # Đảm bảo rằng chỉ sinh viên đã đăng nhập mới có thể truy cập trang này
    if 'giangvien_id' not in request.session:
        # Chưa đăng nhập, chuyển hướng về trang đăng nhập
        return redirect('login_gv')
    
    # Lấy thông tin sinh viên dựa vào MSSV lưu trong session
    msgv = request.session.get('giangvien_id')
    giangvien = Giangvien.objects.get(msgv=msgv)
    
    # Lấy danh sách thời khóa biểu của sinh viên
    lich_day_gv = Lichhoc.objects.filter(giang_vien=msgv)
    
    # Truyền dữ liệu cần thiết về template
    context = {
        'giangvien': giangvien,
        'lich_day_gv': lich_day_gv,
    }
    return render(request, 'app/xem_lich_day_giang_vien.html', context)



def trang_chon_mon(request, msgv):
    
    giangvien = get_object_or_404(Giangvien, msgv=msgv)
    lich_day_giang_vien = Lichhoc.objects.filter(giang_vien=giangvien)
    danh_sach_mon_hoc = [tkb.monhoc for tkb in lich_day_giang_vien]

    return render(request, 'app/trang_chon_mon.html', {
        'giangvien': giangvien,
        'danh_sach_mon_hoc': danh_sach_mon_hoc
    })

def trang_lop_hoc(request, ma_mon, msgv):
    mon_hoc = get_object_or_404(Monhoc, ma_mon=ma_mon)
    giangvien = get_object_or_404(Giangvien, msgv=msgv)
    lop_hoc_phan = Lichhoc.objects.filter(monhoc=mon_hoc)

    
    context =  {
        'giangvien': giangvien,
        'mon_hoc': mon_hoc,
        'lop_hoc_phan': lop_hoc_phan,
    }
    
    return render(request, 'app/trang_lop_hoc.html', context)
    
    




def xem_diem_giang_vien(request, slug_lop, msgv):
    
    giangvien = get_object_or_404(Giangvien, msgv=msgv)
    lop_hoc = get_object_or_404(Lophoc, slug_lop=slug_lop)
    sinhvien_trong_lop = Sinhvien.objects.filter(hoclop=lop_hoc)
    diem_lop = Bangdiem.objects.filter(lop=lop_hoc)
    
    
    context = {
        'giangvien': giangvien,
        'diem_lop': diem_lop,
        'lop_hoc': lop_hoc,
        'sinhvien_trong_lop': sinhvien_trong_lop,
        
    }
    
    return render(request, 'app/xem_diem_giang_vien.html', context)

# Sinh Viên
# Đăng nhập Sinh Viên

def login_SV(request):
    if request.method == "POST":
        mssv = request.POST.get('mssv')
        password_sv = request.POST.get('password_sv')
        sinhvien = Sinhvien.objects.filter(mssv=mssv).first()
        if sinhvien and sinhvien.password_sv == password_sv:
        # Đăng nhập thành công
            request.session['sinhvien_id'] = sinhvien.mssv
            sinh_vien_url = reverse('trang_sinh_vien', kwargs={'mssv': sinhvien.mssv})
            return redirect(sinh_vien_url)
        else:
            messages.info(request, 'MSSV hoặc Mật Khẩu không đúng!')
    return render(request, 'app/dang_nhap_cua_sinh_vien.html') 

# Trang chủ Sinh Viên
def trang_sinh_vien(request, mssv):
    # Đảm bảo rằng chỉ giảng viên đã đăng nhập mới có thể truy cập trang này
    if 'sinhvien_id' not in request.session:
        # Chưa đăng nhập, chuyển hướng về trang đăng nhập
        return redirect('login_sv')
    # Lấy thông tin giảng viên dựa vào MSGV lưu trong session
    mssv = request.session.get('sinhvien_id')
    sinhvien = Sinhvien.objects.get(mssv=mssv)
    # Truyền dữ liệu cần thiết về template
    context = {
        'sinhvien': sinhvien,
    }
    return render(request, 'app/trang_sinh_vien.html', context)


def thongtin_SV(request, mssv):
    # Lấy thông tin sinh viên dựa vào 'mssv' từ session
    mssv = request.session.get('sinhvien_id')
    sinhvien = Sinhvien.objects.get(mssv=mssv)
    # Truyền dữ liệu cần thiết về template
    context = {'sinhvien': sinhvien}
    return render(request, 'app/thong_tin_sinh_vien.html', context)

def xem_diem_sinh_vien(request,mssv):
    # Đảm bảo rằng chỉ sinh viên đã đăng nhập mới có thể truy cập trang này
    if 'sinhvien_id' not in request.session:
        # Chưa đăng nhập, chuyển hướng về trang đăng nhập
        return redirect('login_sv')
    
    # Lấy thông tin sinh viên dựa vào mssv lưu trong session
    mssv = request.session.get('sinhvien_id')
    sinhvien = Sinhvien.objects.get(mssv=mssv)
    
    # Lấy danh sách các điểm môn học của sinh viên
    diem_mon_hoc = Bangdiem.objects.filter(sinhvien=sinhvien)
    
    context = {
        'sinhvien': sinhvien,
        'diem_mon_hoc': diem_mon_hoc
    }
    
    return render(request, 'app/xem_diem_sinh_vien.html', context)



def xem_lich_hoc_sv(request, mssv):
    # Đảm bảo rằng chỉ sinh viên đã đăng nhập mới có thể truy cập trang này
    if 'sinhvien_id' not in request.session:
        # Chưa đăng nhập, chuyển hướng về trang đăng nhập
        return redirect('login_sv')
    
    # Lấy thông tin sinh viên dựa vào MSSV lưu trong session
    mssv = request.session.get('sinhvien_id')
    sinhvien = Sinhvien.objects.get(mssv=mssv)
    
    # Lấy danh sách thời khóa biểu của sinh viên
    lich_hoc_sv = Lichhoc.objects.filter(lophocmon=sinhvien.hoclop)
    
    # Truyền dữ liệu cần thiết về template
    context = {
        'sinhvien': sinhvien,
        'lich_hoc_sv': lich_hoc_sv,
    }
    return render(request, 'app/xem_lich_hoc.html', context)