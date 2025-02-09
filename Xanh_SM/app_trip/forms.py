from django import forms
from app_admin.models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'driver', 
            'students', 
            'start_location', 
            'end_location', 
            'start_time',
            'end_time', 
            'status', 
            'distance',
            'price'
        ]
        
    def clean_distance(self):
        distance = self.cleaned_data.get('distance')
        if distance is not None and distance < 0:
            raise forms.ValidationError("Khoảng cách không thể nhỏ hơn 0.")  # Ghi đè lỗi tiếng Anh
        return distance
