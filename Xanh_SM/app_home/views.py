from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import DriverForm, StudentForm
from app_admin.models import Student, Driver, Trip
from django.core.exceptions import ValidationError
from django.contrib import messages
from datetime import date

def home(request):
    # Thống kê số lượng xe máy & ô tô
    motorcycle_count = Driver.objects.filter(vehicle_type="Bike").count()
    car_count = Driver.objects.filter(vehicle_type="Car").count()

    # Thống kê số tài xế nam & nữ
    male_drivers = Driver.objects.filter(gender="Nam").count()
    female_drivers = Driver.objects.filter(gender="Nữ").count()

    # Thống kê số chuyến đi trong ngày hôm nay
    today = date.today()
    trips_per_hour = []
    for hour in range(24):
        count = Trip.objects.filter(start_time__date=today, start_time__hour=hour).count()
        trips_per_hour.append(count)

    context = {
        "motorcycle_count": motorcycle_count,
        "car_count": car_count,
        "male_drivers": male_drivers,
        "female_drivers": female_drivers,
        "trips_per_hour": trips_per_hour,
    }
    return render(request, "home.html", context)


#Driver
def driver(request):
    drivers = Driver.objects.all()  # Lấy tất cả tài xế từ cơ sở dữ liệu
    return render(request, 'app_home/Driver/driver.html', {'drivers': drivers})

def register_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        messages.success(request, "🚗 Mới có 1 tài xế đã đăng ký!")

        revenue = request.POST.get('revenue')
        driver_id = request.POST.get('driver_id')
        license_number = request.POST.get('license_number')
        phone = request.POST.get('phone')
        my_wallet = request.POST.get('my_wallet')  
        
        # Kiểm tra điều kiện revenue không âm
        if revenue is not None and float(revenue) < 0:
            form.add_error('revenue', 'Doanh thu không được âm!')

        # Kiểm tra điều kiện driver_id có đúng 12 số không
        if driver_id and (len(driver_id) != 12 or not driver_id.isdigit()):
            form.add_error('driver_id', 'Mã tài xế phải có 12 chữ số!')

        # Kiểm tra điều kiện license_number có đúng 8 số không
        if license_number and (len(license_number) != 8 or not license_number.isdigit()):
            form.add_error('license_number', 'Số giấy phép lái xe phải có 8 chữ số!')

        # Kiểm tra điều kiện phone có đúng 10 số không
        if phone and (len(phone) != 10 or not phone.isdigit()):
            form.add_error('phone', 'Số điện thoại phải có 10 chữ số!')

        # Kiểm tra điều kiện wallet có đúng 10 số không
        if my_wallet and (len(my_wallet) != 10 or not my_wallet.isdigit()):
            form.add_error('my_wallet', 'Ví điện tử phải có đúng 10 chữ số!')

        if form.errors:
            return render(request, 'app_home/Driver/register_driver.html', {'form': form})

        if form.is_valid():
            form.save()
            return redirect('driver') 

    else:
        form = DriverForm()

    return render(request, 'app_home/Driver/register_driver.html', {'form': form})


def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)

    if request.method == "POST":
        form = DriverForm(request.POST, instance=driver)

        # Kiểm tra điều kiện revenue không âm
        try:
            revenue = float(request.POST['revenue'])
            if revenue < 0:
                form.add_error('revenue', 'Doanh thu không được âm!')
        except ValueError:
            form.add_error('revenue', 'Doanh thu phải là một số hợp lệ!')

        # Kiểm tra điều kiện driver_id có đúng 12 số không
        driver_id_value = request.POST['driver_id']
        if len(driver_id_value) != 12 or not driver_id_value.isdigit():
            form.add_error('driver_id', 'Mã tài xế phải có 12 chữ số!')

        # Kiểm tra điều kiện license_number có đúng 8 số không
        license_number = request.POST['license_number']
        if len(license_number) != 8 or not license_number.isdigit():
            form.add_error('license_number', 'Số giấy phép lái xe phải có 8 chữ số!')

        # Kiểm tra điều kiện phone có đúng 10 số không
        phone = request.POST['phone']
        if len(phone) != 10 or not phone.isdigit():
            form.add_error('phone', 'Số điện thoại phải có 10 chữ số!')

        # Kiểm tra điều kiện wallet có đúng 10 số không
        my_wallet = request.POST.get('my_wallet')
        if my_wallet and (len(my_wallet) != 10 or not my_wallet.isdigit()):
            form.add_error('my_wallet', 'Ví điện tử phải có đúng 10 chữ số!')

        if form.errors:
            return render(request, 'app_home/Driver/driver_edit.html', {'form': form, 'driver': driver})

        # Nếu không có lỗi, cập nhật thông tin tài xế và lưu lại
        driver.user = form.cleaned_data['user']
        driver.driver_id = form.cleaned_data['driver_id']
        driver.vehicle_type = form.cleaned_data['vehicle_type']
        driver.license_number = form.cleaned_data['license_number']
        driver.phone = form.cleaned_data['phone']
        driver.gender = form.cleaned_data['gender']
        driver.health_status = form.cleaned_data['health_status']
        driver.revenue = revenue
        driver.my_wallet = form.cleaned_data['my_wallet']  
        driver.save()

        return redirect('driver')

    else:
        form = DriverForm(instance=driver)

    return render(request, 'app_home/Driver/driver_edit.html', {'form': form, 'driver': driver})


def delete_driver(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    if request.method == "POST":
        driver.delete()
        return redirect('driver')
        
    return render(request, 'app_home/Driver/driver_delete.html', {'driver': driver})


#Student
def student_list(request):
    students = Student.objects.all()
    return render(request, 'app_home/Student/student.html', {'students': students})

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        messages.success(request, "👨‍🎓 Mới có 1 học sinh đã đăng ký!")

        # Kiểm tra phone (10 chữ số)
        phone = request.POST.get('phone')
        if phone and (len(phone) != 10 or not phone.isdigit()):
            form.add_error('phone', 'Số điện thoại phải có 10 chữ số!')

        # Kiểm tra balance (là số và không âm)
        balance = request.POST.get('balance')
        try:
            balance = float(balance)
            if balance < 0:
                form.add_error('balance', 'Số dư không được âm!')
        except ValueError:
            form.add_error('balance', 'Số dư phải là một số hợp lệ!')

        # Lấy giá trị wallet từ request.POST
        my_wallet = request.POST.get('my_wallet')
        if my_wallet and (len(my_wallet) != 10 or not my_wallet.isdigit()):
            form.add_error('my_wallet', 'Ví điện tử phải có 10 chữ số!')

        # Nếu form có lỗi, trả lại form với lỗi
        if form.errors:
            return render(request, 'app_home/Student/register_student.html', {'form': form})

        # Nếu form hợp lệ, lưu thông tin sinh viên
        if form.is_valid():
            form.save()
            return redirect('student')
    else:
        form = StudentForm()

    return render(request, 'app_home/Student/register_student.html', {'form': form})


def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    
    if request.method == "POST":
        # Kiểm tra phone (10 chữ số)
        phone = request.POST.get('phone')
        if phone and (len(phone) != 10 or not phone.isdigit()):
            form.add_error('phone', 'Số điện thoại phải có 10 chữ số!')

        # Kiểm tra balance (là số và không âm)
        balance = request.POST.get('balance')
        try: 
            balance = float(balance)
            if balance < 0:
                form.add_error('balance', 'Số dư không được âm!')
        except ValueError:
            form.add_error('balance', 'Số dư phải là một số hợp lệ!')

        # Lấy giá trị wallet từ request.POST
        my_wallet = request.POST.get('my_wallet')
        if my_wallet and (len(my_wallet) != 10 or not my_wallet.isdigit()):
            form.add_error('my_wallet', 'Ví điện tử phải có 10 chữ số!')

        # Nếu form có lỗi, trả lại form với lỗi
        if form.errors:
            return render(request, 'app_home/Student/student_edit.html', {'student': student, 'form': form})

        # Lưu các thay đổi nếu không có lỗi
        student.user = request.POST['user']
        student.gender = request.POST['gender']
        student.phone = phone
        student.balance = balance
        student.my_wallet = my_wallet
        student.save()
        
        return redirect('student')
    
    return render(request, 'app_home/Student/student_edit.html', {'student': student, 'form': form})


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student')
    return render(request, 'app_home/Student/student_delete.html', {'student': student})

