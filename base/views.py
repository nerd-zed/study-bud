from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .form import RoomForm

# Create your views here.
rooms = [
    {'id': 1, 'name': 'Room 1', 'description': 'Room 1 description', },
    {'id': 2, 'name': 'Room 2', 'description': 'Room 2 description', },
    {'id': 3, 'name': 'Room 3', 'description': 'Room 3 description', },
]


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


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
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


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'room': room})
