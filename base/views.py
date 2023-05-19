from django.shortcuts import render, redirect
from .models import Room
from .form import RoomForm

# Create your views here.
rooms = [
    {'id': 1, 'name': 'Room 1', 'description': 'Room 1 description', },
    {'id': 2, 'name': 'Room 2', 'description': 'Room 2 description', },
    {'id': 3, 'name': 'Room 3', 'description': 'Room 3 description', },
]


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    print(rooms)
    return render(request, 'base/home.html', context=context)


def room(request, pk):
    print('printing pk: %s' % pk)
    current_room = Room.objects.get(id=pk)
    context = {'room': current_room}
    return render(request, 'base/room.html', context=context)


def createRoom(request):
    room_form = RoomForm()
    if request.method == 'POST':
        room_form = RoomForm(request.POST)
        if room_form.is_valid():
            room_form.save()
            return redirect('home')

    context = {'form': room_form}
    return render(request, 'base/room_form.html', context=context)
