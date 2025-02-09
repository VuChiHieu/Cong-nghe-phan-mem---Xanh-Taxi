from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from app_admin.models import Trip, Driver, Student
from .forms import TripForm
from django.contrib import messages

def trip(request):
    trips = Trip.objects.all()
    return render(request, 'app_home/Trip/trip.html', {'trips': trips})

def add_trip(request):
    drivers = Driver.objects.all()  # Lấy danh sách tài xế
    students = Student.objects.all()  # Lấy danh sách học sinh

    if request.method == 'POST':
        form = TripForm(request.POST)
        messages.success(request, "🧳 Mới có 1 chuyến đi mới!")
        if form.is_valid():
            trip = form.save(commit=False)  # Tạo đối tượng Trip nhưng chưa lưu
            selected_students = form.cleaned_data.get('students')  # Lấy danh sách học sinh từ form
            
            # Tính giá tiền dựa trên khoảng cách
            trip.price = trip.distance * 10000  

            # Kiểm tra giá tiền không được nhỏ hơn 0
            if trip.price < 0:
                form.add_error('price', 'Giá tiền không thể nhỏ hơn 0.')
            # Kiểm tra thời gian kết thúc hợp lệ
            elif trip.end_time and trip.start_time and trip.end_time <= trip.start_time:
                form.add_error('end_time', 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu.')
            else:
                trip.save()  # Lưu đối tượng Trip nếu không có lỗi
                form.save_m2m()  # Lưu quan hệ Many-to-Many với học sinh
                return redirect('trip')

    else:
        form = TripForm()

    return render(request, 'app_home/Trip/add_trip.html', {
        'form': form,
        'drivers': drivers,
        'students': students,
    })

def edit_trip(request, id):
    trip = get_object_or_404(Trip, id=id)
    drivers = Driver.objects.all()
    students = Student.objects.all()

    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        messages.success(request, "🚌 Mới có 1 chuyến đi mới!")
        if form.is_valid():
            updated_trip = form.save(commit=False)

            # Cập nhật thông tin nhưng giữ lại giá trị cũ nếu không có thay đổi
            trip.start_location = request.POST.get('start_location', trip.start_location)
            trip.end_location = request.POST.get('end_location', trip.end_location)
            trip.start_time = request.POST.get('start_time', trip.start_time)
            trip.end_time = request.POST.get('end_time', trip.end_time)
            trip.status = request.POST.get('status', trip.status)

            # Tính lại giá tiền dựa trên khoảng cách
            trip.price = trip.distance * 10000  

            # Kiểm tra điều kiện hợp lệ trước khi lưu
            if trip.price < 0:
                form.add_error('price', 'Giá tiền không thể nhỏ hơn 0.')
            elif trip.end_time and trip.start_time and trip.end_time <= trip.start_time:
                form.add_error('end_time', 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu.')
            else:
                trip.save()
                form.save_m2m()
                return redirect('trip')

    else:
        form = TripForm(instance=trip)

    return render(request, 'app_home/Trip/edit_trip.html', {
        'form': form,
        'drivers': drivers,
        'students': students,
    })
    
# Xóa chuyến đi
def delete_trip(request, id):
    trip = get_object_or_404(Trip, id=id)
    if request.method == 'POST':
        trip.delete()
        return redirect('trip')

    return render(request, 'app_home/Trip/delete_trip.html', {
        'trip': trip,
    })