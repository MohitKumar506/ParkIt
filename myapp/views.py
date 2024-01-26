from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import mapPointers, myBooking1

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
                user.save();
                return redirect('register')
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
        curr.save()
        return redirect('pdashboard')
    else:
        return render(request, 'provider.html')


def pdashboard(request):
    lists = mapPointers.objects.filter(user = request.user.id)
    return render(request,'pdashboard.html',locals())

def delLocation(request,pk=None):
    hw = get_object_or_404(mapPointers, id=pk)
    hw.delete()
    return redirect("pdashboard")


def show(request):
    lists = mapPointers.objects.filter(user = request.user.id)
    return render(request, 'show.html',locals())

def need(request):
    lists = mapPointers.objects.all()
    return render(request, 'need.html',locals())

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
        new_booking.save()
        
        curr.delete()
        return redirect('need')
    except mapPointers.DoesNotExist:
        return redirect('need')


def book(request):
    lists = myBooking1.objects.filter(user = request.user)
    return render(request,'book.html',locals())

def find(request,id):
    curr = myBooking1.objects.get(id = id)
    latitude = curr.latitude
    longitude = curr.longitude
    return render(request, 'find.html',locals())

def tripOver(request,id):
    try:
        curr = get_object_or_404(myBooking1, id=id)
        
        new_booking = mapPointers()
        new_booking.user = curr.user
        new_booking.photo = curr.photo 
        new_booking.rate = curr.rate  
        new_booking.latitude = curr.latitude  
        new_booking.longitude = curr.longitude  
        new_booking.save()
        
        curr.delete()
        return redirect('book')
    except mapPointers.DoesNotExist:
        return redirect('book')
