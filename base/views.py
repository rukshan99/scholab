from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

def home(request):
    q = request.GET.get('q') or ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'topics': topics
    }
    return render(request, 'base/home.html', context)

def room(request, id):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_view')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home_view')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if request.method == 'POST':
        room.delete()
        return redirect('home_view')
    return render(request, 'base/delete.html', {'obj': room})