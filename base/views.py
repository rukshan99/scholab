from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

def loginView(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home_view')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
       
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutView(request):
    logout(request)
    return redirect('home_view')

def registerView(request):
    page = 'register'
    form = UserCreationForm()
    context = {
        'page': page,
        'form': form
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home_view')
        else:
            messages.error(request, 'An error occured during registration.')
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') or ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_activity = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_activity': room_activity
    }
    return render(request, 'base/home.html', context)

def room(request, id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        if request.user.is_authenticated == False:
            messages.error(request, 'You need to login first.')
            return render(request, 'base/login_register.html', {'page': 'login'})
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room_view', id=room.id)
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)

def profileView(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    user_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'room_activity': user_messages,
        'topics': topics
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login_view')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        room.participants.add(request.user)
        room.save()
        return redirect('home_view')
    context = {
        'form': form,
        'topics': topics
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login_view')
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room.')
    
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home_view')
    context = {
        'form': form,
        'topics': topics,
        'room': room
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login_view')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room.')

    if request.method == 'POST':
        room.delete()
        return redirect('home_view')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login_view')
def deleteMessage(request, id):
    message = Message.objects.get(id=id)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message.')

    if request.method == 'POST':
        message.delete()
        try:
            user_message = Message.objects.get(user=message.user, room=message.room)
        except Message.DoesNotExist:
            user_message = None
        if user_message is None:
            message.room.participants.remove(message.user)
        return redirect('room_view', id=message.room.id)
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login_view')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.username = request.POST.get('username').lower()
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('profile_view', id=user.id)
    else:
        print(form.errors.as_data())
    return render(request, 'base/update_user.html', {'form': form})
