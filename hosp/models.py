from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    department=models.CharField(max_length=200)

class Doctor(models.Model):
    name =models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255) 
    age=models.IntegerField()
    number=models.CharField(max_length=255)  
    image=models.ImageField(upload_to="image/")   

class usermember(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    doc_name = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255) 
    age=models.IntegerField()
    number=models.CharField(max_length=255)  
    image=models.ImageField(upload_to="image/")  

class Room(models.Model):
    model = models.CharField(max_length=255) 
    charge =models.PositiveIntegerField()
    image=models.ImageField(upload_to="image/")  

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    )

    patient_name = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')


class Billdetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    admit_date = models.DateField()
    discharge_date = models.DateField()
    total_days = models.PositiveIntegerField()
    total_charge = models.PositiveIntegerField()
