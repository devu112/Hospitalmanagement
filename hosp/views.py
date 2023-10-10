from django.shortcuts import render, redirect
from .models import Department, Doctor ,usermember,Appointment,Room,Billdetails
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
import random
import string
import re
import os
from .forms import AppointmentForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import PasswordResetForm
from datetime import datetime
from django.urls import reverse




def home(request):
    return render(request, 'home.html')

def addDep(request):
    dept = Department.objects.all()
    return render(request, 'addDep.html', {'dept': dept })

def addDoc(request):
    dept = Department.objects.all()
    return render(request, 'addDoc.html', {'dept': dept})

def deptdb(request):
    if request.method == 'POST':
        dept = request.POST['dept']
        department = Department(department=dept)
        department.save()
        return render(request, 'addDep.html', {'show_popup': True})
    else:
        return render(request, 'addDep.html', {'show_popup': False})

def adminhome(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'adminhome.html')

def adminlog(request):
    if request.method == "POST":
        username = request.POST['name']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('adminhome')
            else:
                login(request, user)
                messages.info(request, f'Welcome {username}')
                return redirect('userhome')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/')
    return render(request, 'home.html')

@login_required
def userhome(request):
    dept = Department.objects.all()
    doctors = Doctor.objects.all()
    user_profile = None
    if request.user.is_authenticated:
        current_user = request.user.id
        user_profile = usermember.objects.get(user_id=current_user)
    return render(request, 'userhome.html', {'departments': dept, 'doctors': doctors,'users':user_profile})

def doctordb(request):
    if request.method == 'POST':
        name = request.POST['dname']
        address = request.POST['add']
        depat = request.POST['depat']
        dept = Department.objects.get(id=depat)
        age = request.POST['age']
        number = request.POST['num']
        image = request.FILES.get('file')
        doctor = Doctor(name=name, address=address, department=dept, age=age, number=number, image=image)
        doctor.save()
        return render(request, 'addDoc.html', {'show_popup': True})
    else:
        return render(request, 'addDoc.html', {'show_popup': False})
    

def signin(request):
    return render(request,'signin.html')


def signup(request):
     return render(request,'signup.html')

# def usereg(request):
#     fname=request.POST.get('fname')
#     lname=request.POST.get('lname')
#     uname=request.POST.get('uname')
#     pswd=request.POST.get('psw')
#     cpswd=request.POST.get('cpsw')
#     add=request.POST.get('add')
#     age=request.POST.get('age')
#     email=request.POST.get('email')
#     number=request.POST.get('number')
#     image=request.FILES.get('file')
#     if pswd==cpswd:
#         if User.objects.filter(username=uname).exists():
#             messages.info(request,'username already exists!')
#             return redirect('signup')
#         else:
#             user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=pswd,email=email)
#             user.save()
#             u=User.objects.get(id=user.id)
#             member=usermember(address=add,age=age,number=number,image=image,user=u)
#             member.save()
#             subject="Registration Completed"
#             message=f"your username is {uname} and password is {pswd}"
#             recipient=request.POST['email']
#             send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
#             return redirect('/')
            
#     else:
#         messages.info(request,'password doesnt match!')
#         return redirect('signup')



def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def usereg(request):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    uname = request.POST.get('uname').capitalize()  # Capitalizeirst letter
    js_generated_pswd = request.POST.get('psw')
    add = request.POST.get('add')
    age = request.POST.get('age')
    email = request.POST.get('email')
    number = request.POST.get('number')
    image = request.FILES.get('file')
    if User.objects.filter(username=uname).exists():
            messages.info(request,'username already exists!')
            return redirect('signup')

    # Validate username
    if not re.match(r'^[A-Z][a-zA-Z0-9_]*$', uname):
        messages.error(request, 'Invalid username format. The first letter should be capital.')
        return redirect('signup')

    # Validate contact number
    if not re.match(r'^\d{10}$', number):
        messages.error(request, 'Invalid contact number. It should contain exactly 10 digits.')
        return redirect('signup')

    
    user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, password=js_generated_pswd, email=email)
    user.save()
    u=User.objects.get(id=user.id)
    member=usermember(address=add,age=age,number=number,image=image,user=u)
    member.save()
    subject="Registration Completed"
    message=f"your username is {uname} and password is {js_generated_pswd}"
    recipient=request.POST['email']
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
    return redirect('signin')

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Password reset email has been sent. Please check your email.')
            return redirect('signin')
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})
   








# def usereg(request):
#     fname = request.POST.get('fname')
#     lname = request.POST.get('lname')
#     uname = request.POST.get('uname').capitalize()  # Capitalize the first letter
#     pswd = generate_random_password()
#     cpswd = request.POST.get('cpsw')  # Generate random password
#     add = request.POST.get('add')
#     age = request.POST.get('age')
#     email = request.POST.get('email')
#     number = request.POST.get('number')
#     image = request.FILES.get('file')

#     if pswd != cpswd:
#         messages.error(request, 'Passwords do not match. Please enter the same password in both fields.')
#         return render(request, 'signup.html')  # Render the same page with error message

#     # Check if the username already exists (case-insensitive)
#     if User.objects.filter(username__iexact=uname).exists():
#         messages.error(request, 'Username already exists!')
#         return redirect('signup')

#     try:
#         user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, password=pswd, email=email)
#         user.save()

#         u = User.objects.get(id=user.id)
#         member = usermember(address=add, age=age, number=number, image=image, user=u)
#         member.save()

#         subject = "Registration Completed"
#         message = f"Your username is {uname} and password is {pswd}"
#         recipient = request.POST['email']
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

#         messages.success(request, 'Registration successful. Your username and password have been sent to your email.')
#         return redirect('signin')
#     except Exception as e:
#         messages.error(request, f"An error occurred during registration: {e}")
#         return render(request, 'signup.html')


def showDoc(request):
    if request.user.is_authenticated:
        doc=Doctor.objects.all()
        return render(request,'showDoc.html',{'docs':doc})
    return redirect('/')
def delete(request,pk):
    doc1=Doctor.objects.get(id=pk)
    doc1.delete()
    return redirect('showDoc')
def edit(request,pk):
    doc1=Doctor.objects.get(id=pk)
    dept=Department.objects.all()
    return render(request,'edit.html',{'s':doc1, 'dept':dept})

def editdb(request,pk):
    if request.method=='POST':
        doctor1=Doctor.objects.get(id=pk)
        doctor1.name=request.POST['dname']
        doctor1.address=request.POST['add']
        doctor1.age=request.POST['age']
        doctor1.number=request.POST['num']
        if 'image' in request.FILES:
            doctor1.image = request.FILES['image']
        depat=request.POST['depat']
        dept=Department.objects.get(id=depat)
        doctor1.department=dept
        doctor1.save()
        return redirect('showDoc')
    return render(request,'edit.html')



def showP(request):
    if request.user.is_authenticated:
        user1=usermember.objects.all()
        return render(request,'showP.html',{'users':user1})
    return redirect('/')

def profile(request):
    if request.user.is_authenticated:
        currentuser = request.user.id
        user1 = usermember.objects.get(user_id=currentuser)
        return render(request,'profile.html',{'users':user1})
def showda(request):
    if request.user.is_authenticated:
        doc=Doctor.objects.all()
        return render(request,'showda.html',{'docs':doc})
    return redirect('/')

# def edit2(request):
#     if request.user.is_authenticated:
#         currentuser = request.user.id
#         user1 = usermember.objects.get(user_id=currentuser)
#         user2 = User.objects.get(id=currentuser)
#         if request.method == 'POST':
#             if len(request.FILES)!=0:
#                 if len(user1.image)>0:
#                     os.remove(user1.image.path)
#                 user1.image=request.FILES.get('file')
#             user2.first_name=request.POST.get('fname') 
#             user2.last_name=request.POST.get('lname')   
#             user2.username=request.POST.get('uname') 
#             user2.password=request.POST.get('psw')     
#             user2.email=request.POST.get('email')   
#             user1.age=request.POST.get('age')
#             user1.address=request.POST.get('add')   
#             user1.number=request.POST.get('number')  
#             user1.save()
#             user2.save()
#             return redirect('profile')
#         return render(request,'edit2.html',{'u':user1}) 



def edit2(request):
    if request.user.is_authenticated:
     currentuser = request.user
     user1 = usermember.objects.get(user=currentuser)
    if request.method == 'POST':
        if request.FILES.get('file'):
            if user1.image:  # If there's an existing image, delete it before saving the new one
                os.remove(user1.image.path)
            user1.image = request.FILES.get('file')
        user1.age = request.POST.get('age')
        user1.address = request.POST.get('add')
        user1.number = request.POST.get('number')
        user1.save()

        # Update user fields using the User model
        currentuser.first_name = request.POST.get('fname')
        currentuser.last_name = request.POST.get('lname')
        currentuser.username = request.POST.get('uname')
        currentuser.email = request.POST.get('email')
        currentuser.save()

        return redirect('profile')

    return render(request, 'edit2.html', {'u': user1})
# def appointmentdb(request):
#     if request.method=='POST':
#         sel = request.POST['sel']
#         doc1=Doctor.objects.get(id=sel)
#         name=request.POST['name']
#         mobile=request.POST['name']
#         email=request.POST['name']

def appointment(request):
    # Fetch the list of doctors in the dropdown
    doctors = Doctor.objects.all()
    return render(request, 'appointment.html', {'doctors': doctors})



# def appointmentdb(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             doctor = form.cleaned_data['doctor_name']
#             appointment = form.save(commit=False)
#             appointment.doctor_name = doctor
#             appointment.save()
#             messages.success(request, 'Your appointment has been registered.Kindly wait for the approval')
#             return redirect('showstatus')  

#     else:
#         form = AppointmentForm()

#     # Fetch the list of doctors to populate the dropdown
#     doctors = Doctor.objects.all()

#     return render(request, 'appointment.html', {'form': form, 'doctors': doctors})








# def showstatus(request):
#     if request.user.is_authenticated:
#         user = request.user

#         # Fetch all appointments for the currently logged-in user with status 'PENDING', 'APPROVED', or 'REJECTED'
#         user_appointments = Appointment.objects.filter(Q(patient_name=user) & Q(status__in=['PENDING', 'APPROVED', 'REJECTED']))

#         return render(request, 'showstatus.html', {'appointments': user_appointments})

#     # Redirect to a login page or any other page if the user is not logged in
#     return redirect('signin')  # Replace 'signin' with the URL name of the login page



def pending_appointments(request):
    pending_appointments = Appointment.objects.filter(status='PENDING')
    return render(request, 'pending_appointments.html', {'appointments': pending_appointments})




# def approve_appointment(request, appointment_id):
#     appointment = Appointment.objects.get(id=appointment_id)
#     appointment.status = 'APPROVED'
#     appointment.save()
#     return redirect('showstatus')

# def reject_appointment(request, appointment_id):
    
#    if request.method=='POST':
#     appointment = Appointment.objects.get(id=appointment_id)
#     appointment.status = 'REJECTED'
#     appointment.save()
#     return redirect('showstatus')




# def showstatus(request):
#     if request.user.is_authenticated:
#         user = request.user
#         # Fetch pending appointments for the currently logged-in user
#         pending_appointments = Appointment.objects.filter(patient_name=user, status='PENDING')

#         # Check if there's a query parameter indicating the action taken by the admin
#         action = request.GET.get('action')
#         if action:
#             if action == 'approved':
#                 # Update the status to 'APPROVED' for the approved appointment
#                 appointment_id = request.GET.get('appointment_id')
#                 try:
#                     appointment = Appointment.objects.get(id=appointment_id)
#                     appointment.status = 'APPROVED'
#                     appointment.save()
#                 except Appointment.DoesNotExist:
#                     pass  # Handle the case where the appointment with the given ID does not exist

#             elif action == 'rejected':
#                 # Update the status to 'REJECTED' for the rejected appointment
#                 appointment_id = request.GET.get('appointment_id')
#                 try:
#                     appointment = Appointment.objects.get(id=appointment_id)
#                     appointment.status = 'REJECTED'
#                     appointment.save()
#                 except Appointment.DoesNotExist:
#                     pass  # Handle the case where the appointment with the given ID does not exist

#         return render(request, 'showstatus.html', {'appointments': pending_appointments})

#     # Redirect to a login page or any other page if the user is not logged in
#     return redirect('signin')  # Replace 'signin' with the URL name of the login page

# def approve_appointment(request, appointment_id):
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#         appointment.status = 'APPROVED'
#         appointment.save()
#         # Add a success message to indicate that the appointment has been approved
#         messages.success(request, "Appointment has been approved.")
#     except Appointment.DoesNotExist:
#         # Handle the case where the appointment with the given ID does not exist
#         messages.error(request, "Appointment not found.")

#     # Redirect back to the pending appointments page
#     return redirect('pending_appointments')
# def reject_appointment(request, appointment_id):
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#         appointment.status = 'REJECTED'
#         appointment.save()
#         # Add a success message to indicate that the appointment has been rejected
#         messages.success(request, "Appointment has been rejected.")
#     except Appointment.DoesNotExist:
#         # Handle the case where the appointment with the given ID does not exist
#         messages.error(request, "Appointment not found.")

#     # Redirect back to the pending appointments page
#     return redirect('pending_appointments')




# @login_required
# def showstatus(request):
#     # Fetch appointments for the currently logged-in user
#     appointments = Appointment.objects.filter(patient_name=request.user.username)
#     return render(request, 'showstatus.html', {'appointments': appointments})


from django.http import HttpResponse

def appointmentdb(request):
    if request.method == 'POST':
        doctors = Doctor.objects.all()
        pname = request.POST['patient_name']
        date = request.POST['date']
        desc = request.POST['description']

        try:
            
            patient_user = User.objects.get(username=pname)
        except User.DoesNotExist:
           
            return HttpResponse("User with the provided username does not exist.")

        # Retrieve a single doctor instance (e.g., the first doctor) from the queryset
        doctor = doctors.first()

        app = Appointment(patient_name=patient_user, doctor_name=doctor, date=date, description=desc)
        app.save()

        # Redirect to the 'showstatus' page after successful registration
        return redirect('showstatus')

   





def approve_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'APPROVED'
    appointment.save()
    return redirect('pending_appointments')

def reject_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'REJECTED'
    appointment.save()
    return redirect('pending_appointments')

def depat(request):
    return render(request,'depat.html')


def addRoom(request):
    room=Room.objects.all()
    return render(request, 'addRoom.html', {'room':room})

def roomdb(request):
    if request.method=="POST":
        model=request.POST['model']
        chrg=request.POST['charge']
        image = request.FILES['image']
        room1=Room(model=model,charge=chrg,image=image)
        room1.save()
        return render(request, 'addRoom.html', {'show_popup': True})
    else:
        return render(request, 'addRoom.html', {'show_popup': False})

def showroom(request):
 if request.user.is_authenticated:
    rooms = Room.objects.all()
    print(rooms)
    return render(request, 'showroom.html', {'rooms': rooms})
 return redirect('/')
   
@login_required
def showstatus(request):
    #Fetch appointments for the currently logged-in user
    appointments = Appointment.objects.filter(patient_name=request.user)
    return render(request, 'showstatus.html', {'appointments': appointments})


def aboutus(request):
    return render(request,'aboutus.html')

def contactus(request):
    return render(request,'contactus.html')

def user_logout(request):
    auth.logout(request)
    return redirect('home')

def depat(request):
    return render(request,'depat.html')





def add_bill(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        room_id = request.POST['room_id']
        admit_date_str = request.POST['admit_date']
        discharge_date_str = request.POST['discharge_date']

        # Convert the date strings to date objects
        admit_date = datetime.strptime(admit_date_str, '%Y-%m-%d').date()
        discharge_date = datetime.strptime(discharge_date_str, '%Y-%m-%d').date()

        user = User.objects.get(id=user_id)
        room = Room.objects.get(id=room_id)

        #Calculate total days and total charge
        total_days = (discharge_date - admit_date).days
        total_charge = room.charge * total_days

        bill = Billdetails(user=user, room=room, admit_date=admit_date, discharge_date=discharge_date, total_days=total_days, total_charge=total_charge)
        bill.save()

        #Redirect to the admin
        return render(request, 'adminbill.html', {'show_popup': True})

    else:
        return render(request, 'adminbill.html', {'show_popup': False})















# views.py
def userbill(request):
    if request.user.is_authenticated:
        user_bills = Billdetails.objects.filter(user=request.user)
        return render(request, 'userbill.html', {'bills': user_bills})

    return redirect('home')  # Redirect to the homepage or login page if the user is not logged in

def adminbill(request):
    users = User.objects.all()
    rooms = Room.objects.all()
    return render(request,'adminbill.html', {'users': users, 'rooms': rooms})