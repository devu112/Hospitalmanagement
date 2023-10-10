from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addDep', views.addDep, name='addDep'),
    path('addDoc', views.addDoc, name='addDoc'),
    path('addRoom', views.addRoom, name='addRoom'),
    
    path('doctordb', views.doctordb, name='doctordb'),
    path('deptdb', views.deptdb, name='deptdb'),
    path('adminlog', views.adminlog, name='adminlog'),
    path('adminhome', views.adminhome, name='adminhome'),
    path('userhome', views.userhome, name='userhome'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('usereg',views.usereg,name='usereg'),
    path('showDoc',views.showDoc,name='showDoc'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('edit/<int:pk>',views.edit,name='edit'),
    path('editdb/<int:pk>',views.editdb,name='editdb'),
    path('profile',views.profile,name='profile'),
    path('showP',views.showP,name='showP'),
    path('showda',views.showda,name='showda'),
    path('edit2',views.edit2,name='edit2'),
    path('appointment',views.appointment,name='appointment'),
    path('appointmentdb', views.appointmentdb, name='appointmentdb'),
    path('showstatus',views.showstatus,name='showstatus'),
    path('pending_appointments/', views.pending_appointments, name='pending_appointments'),
    path('approve_appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject_appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('depat',views.depat,name='depat'),
    path('roomdb',views.roomdb,name='roomdb'),
    path('showroom',views.showroom,name='showroom'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('contactus',views.contactus,name='contactus'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('depat',views.depat,name='depat'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('add_bill/', views.add_bill, name='add_bill'),
    path('userbill/', views.userbill, name='userbill'),
    path('adminbill/', views.adminbill, name='adminbill'),






]
