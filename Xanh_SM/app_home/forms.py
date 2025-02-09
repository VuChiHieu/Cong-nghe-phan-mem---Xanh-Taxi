from django import forms
from app_admin.models import Student, Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user', 'driver_id', 'vehicle_type', 'license_number', 'phone', 'gender', 'health_status', 'revenue', 'my_wallet']

    def clean_driver_id(self):
        driver_id = self.cleaned_data.get('driver_id')
        driver_instance = self.instance  

        if Driver.objects.filter(driver_id=driver_id).exclude(id=driver_instance.id).exists():
            raise forms.ValidationError('Mã tài xế này đã tồn tại!')

        return driver_id

    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        driver_instance = self.instance  

        if Driver.objects.filter(license_number=license_number).exclude(id=driver_instance.id).exists():
            raise forms.ValidationError('Giấy phép lái xe này đã tồn tại!')

        return license_number

    def clean_my_wallet(self):
        my_wallet = self.cleaned_data.get('my_wallet')
        driver_instance = self.instance  

        if Driver.objects.filter(my_wallet=my_wallet).exclude(id=driver_instance.id).exists():
            raise forms.ValidationError('Tài khoản ví này đã tồn tại!')

        return my_wallet


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'gender', 'phone', 'balance', 'my_wallet']

    def clean_my_wallet(self):
        my_wallet = self.cleaned_data.get('my_wallet')
        student_instance = self.instance  

        if Student.objects.filter(my_wallet=my_wallet).exclude(id=student_instance.id).exists():
            raise forms.ValidationError('Tài khoản ví này đã tồn tại!')

        return my_wallet
