from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic, Message
from .form import RoomForm

# Create your views here.
# rooms = [
#     {'id': 1, 'name': 'Room 1', 'description': 'Room 1 description', },
#     {'id': 2, 'name': 'Room 2', 'description': 'Room 2 description', },
#     {'id': 3, 'name': 'Room 3', 'description': 'Room 3 description', },
# ]


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        print("User", user)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
    context = {'page': page}
    return render(request, 'base/login_registration.html', context=context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    page = 'register'

    registerForm = UserCreationForm()

    if request.method == 'POST':
        registerForm = UserCreationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error in User registration')

    context = {'page': page, 'register_form': registerForm}
    return render(request, 'base/login_registration.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    print('================================================================')
    print(q)
    # contains - this will match the substring with the query string
    # i - means case insensitive
    rooms = Room.objects.filter(
        Q(topic__title__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
    )
    # rooms = Room.objects.all()
    topics = Topic.objects.all()
    # print(vars(request))
    print(rooms.count())
    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms.count()}
    # print(rooms)
    return render(request, 'base/home.html', context=context)


def room(request, pk):
    print('printing pk: %s' % pk)
    current_room = Room.objects.get(id=pk)
    room_messages = current_room.message_set.all().order_by('-created')
    participants = current_room.participants.all()

    if request.method == 'POST':
        room_message = Message.objects.create(
            user=request.user,
            room=current_room,
            body=request.POST.get('body'),
        )
        current_room.participants.add(request.user)
        return redirect('room', pk=current_room.id)

    context = {'room': current_room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context=context)


@login_required(login_url='login')
def createRoom(request):
    room_form = RoomForm()
    if request.method == 'POST':
        room_form = RoomForm(request.POST)
        if room_form.is_valid():
            room_form.save()
            return redirect('home')

    context = {'form': room_form}
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user.username != room.host.username:
        return HttpResponse('You are not allowed here.')

    # Here we given the instance to load in the screen
    form = RoomForm(instance=room)

    if request.method == 'POST':
        # if we have not given instance then the new record will be created
        room_form = RoomForm(request.POST, instance=room)
        if room_form.is_valid():
            room_form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user.username != room.host.username:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user.username != message.user.username:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
