from django.contrib import admin
from .models import Driver, Student, Trip

class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'driver_id', 'vehicle_type', 'license_number', 'phone', 'gender', 'health_status','my_wallet','revenue')
    search_fields = ('user', 'phone', 'vehicle_type')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone', 'my_wallet','balance')
    search_fields = ('user', 'phone', 'gender')

class TripAdmin(admin.ModelAdmin):
    list_display = ('driver', 'get_students', 'start_location', 'end_location', 'status', 'distance', 'price', 'start_time', 'end_time')
    list_filter = ('status', 'driver', 'students')  # Lọc theo trạng thái, tài xế và học sinh
    search_fields = ('start_location', 'end_location', 'driver__user', 'students__user')  # Tìm kiếm theo tên tài xế và học sinh

    def get_students(self, obj):
        # Trả về danh sách tên học sinh tham gia chuyến đi
        return ", ".join([student.user for student in obj.students.all()])
    get_students.short_description = 'Students'  # Thay đổi tên hiển thị trong list_display
    
admin.site.register(Driver, DriverAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Trip, TripAdmin)
