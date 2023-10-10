from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor_name', 'patient_name', 'date', 'description']
        # Add any additional widgets or form field customizations here if needed
