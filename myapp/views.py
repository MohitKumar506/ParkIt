from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import mapPointers, myBooking1, Booked, Earning, Previous
from django.shortcuts import render, get_object_or_404, redirect
import uuid
import time

# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                Earning.objects.create(user=user, earning=0)
                return redirect('login')
        else:
            messages.info(request, 'password not same')
            return redirect('register')
    
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username , password = password)

        if user is not None:
            auth.login(request,user)
            return render(request, 'display.html',{'username':username})
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
        

    else:
        return render(request, 'login.html')
    
    
def logout(request):
    auth.logout(request)
    return redirect('login')

def display(request):
    user = request.user
    return render(request, 'display.html')

def need(request):
    return render(request, 'need.html')

def provider(request):
    if request.method == 'POST':
        curr = mapPointers()
        curr.user = request.user
        curr.photo = request.FILES['photo']
        curr.latitude = request.POST['latitude']
        curr.longitude = request.POST['longitude']
        curr.rate = request.POST['rate']
        curr.status = False
        curr.email = request.user.email
        curr.save()
        return redirect('pdashboard')
    else:
        return render(request, 'provider.html')


def pdashboard(request):
    lists = mapPointers.objects.filter(user = request.user)
    earn = Earning.objects.get(user = request.user)
    return render(request,'pdashboard.html',locals())

def delLocation(request,pk=None):
    hw = get_object_or_404(mapPointers, id=pk)
    hw.delete()
    return redirect("profile")


def show(request):
    lists = mapPointers.objects.filter(user = request.user)
    return render(request, 'show.html',locals())

def need(request):
    lists = mapPointers.objects.all()
    return render(request, 'need.html',locals())

# def myBookings(request, id):
#     try:
#         curr = get_object_or_404(mapPointers, id=id)
        
#         new_booking = myBooking1()
#         new_booking.user = request.user
#         new_booking.name = curr.user
#         new_booking.photo = curr.photo 
#         new_booking.rate = curr.rate  
#         new_booking.latitude = curr.latitude  
#         new_booking.longitude = curr.longitude  
#         new_booking.var = curr.id
#         new_booking.save()
        
#         curr.status = True 
#         curr.save() 
#         return redirect('book')
#     except mapPointers.DoesNotExist:
#         return redirect('book')


def book(request):
    lists = myBooking1.objects.filter(user = request.user)
    return render(request,'book.html',locals())

def find(request,id):
    curr = myBooking1.objects.get(id = id)
    latitude = curr.latitude
    longitude = curr.longitude
    return render(request, 'find.html',locals())

def tripOver(request, id):
    try:
        curr = get_object_or_404(myBooking1, id=id)
        
        new_booking = mapPointers(id=curr.var)
        new_booking.user = User.objects.get(username=curr.name)
        new_booking.status = False
        new_booking.photo = curr.photo 
        new_booking.rate = curr.rate  
        new_booking.latitude = curr.latitude  
        new_booking.longitude = curr.longitude
        new_booking.booked_by = "empty"
        new_booking.save()

        past = Previous()
        past.user = request.user
        past.name = User.objects.get(username=curr.name)
        past.latitude = curr.latitude  
        past.longitude = curr.longitude
        past.rate = curr.rate

        past.save()
        
        
        curr.delete()
        return redirect('book')
    except mapPointers.DoesNotExist:
        return redirect('book')

def payment(request):
    return render(request, 'payment.html')

def myBookings(request, id):
    try:
        curr = get_object_or_404(mapPointers, id=id)
        
        new_booking = myBooking1()
        new_booking.user = request.user
        new_booking.name = curr.user
        new_booking.photo = curr.photo 
        new_booking.rate = curr.rate  
        new_booking.latitude = curr.latitude  
        new_booking.longitude = curr.longitude  
        new_booking.var = curr.id
        new_booking.email = curr.email
        new_booking.save()

        earn = Earning.objects.get(user = curr.user)
        earn.earning += curr.rate
        earn.save()
        
        curr.status = True 
        curr.booked_by = request.user.username
        curr.Booked_email = request.user.email
        curr.save()   
        return redirect('payment')
    except mapPointers.DoesNotExist:
        return redirect('book')


def redirecting(request):
    return render(request, 'redirecting.html')

def confirmed(request):
    return render(request, 'confirmed.html')

def profile(request):
    booked = myBooking1.objects.filter(user = request.user)
    myBookings = mapPointers.objects.filter(user = request.user)
    earn = Earning.objects.get(user = request.user)
    user = request.user
    try:
        past = Previous.objects.filter(user=request.user)
    except Previous.DoesNotExist:
        past = None
    return render(request, 'profile.html',locals())

def profileShow(request):
    lists = mapPointers.objects.filter(user = request.user)
    return render(request, 'profileShow.html',locals())
