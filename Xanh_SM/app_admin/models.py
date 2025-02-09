from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator 


class Driver(models.Model):
    user = models.CharField(max_length=100)
    driver_id = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    health_status = models.CharField(max_length=100, blank=True, null=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    my_wallet = models.CharField(max_length=50, blank=True, null=True)  # Wallet là CharField

    def __str__(self):
        return f"{self.user} {self.vehicle_type} {self.phone} {self.gender} {self.my_wallet}"

class Student(models.Model):
    user = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    my_wallet = models.CharField(max_length=50, blank=True, null=True)  # Wallet là CharField

    def __str__(self):
        return f"{self.user} {self.gender} {self.phone} {self.balance} {self.my_wallet}"


class Trip(models.Model):
    STATUS_CHOICES = (
        ('picking_up', 'Đang đón khách'),
        ('ongoing', 'Đang di chuyển'),
        ('completed', 'Hoàn thành'),
        ('canceled', 'Hủy'),
    )

    # Liên kết chuyến đi với tài xế (Driver)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')

    # Liên kết chuyến đi với học sinh (Student), một chuyến đi có thể có nhiều học sinh
    students = models.ManyToManyField(Student, related_name='trips')

    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Trip from {self.start_location} to {self.end_location} with driver {self.driver.user}"
