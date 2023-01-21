from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home_view')
            else:
                messages.error(request, 'Authentication failed. Please check the credentials again.')
        except:
            messages.error(request, 'Authentication failed. Please check the credentials again.')
       
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutView(request):
    logout(request)
    return redirect('home_view')

def home(request):
    q = request.GET.get('q') or ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count
    }
    return render(request, 'base/home.html', context)

def room(request, id):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, 'base/room.html', context)

@login_required(login_url='login_view')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_view')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login_view')
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room.')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home_view')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login_view')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room.')

    if request.method == 'POST':
        room.delete()
        return redirect('home_view')
    return render(request, 'base/delete.html', {'obj': room})