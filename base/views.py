from django.shortcuts import render

# Create your views here.
rooms = [
    {'id': 1, 'name': 'Room 1', 'description': 'Room 1 description', },
    {'id': 2, 'name': 'Room 2', 'description': 'Room 2 description', },
    {'id': 3, 'name': 'Room 3', 'description': 'Room 3 description', },
]


def home(request):
    context = {'rooms': rooms}
    print(rooms)
    return render(request, 'base/home.html', context=context)


def room(request, pk):
    print('printing pk: %s' % pk)
    current_room = ''
    for room in rooms:
        if room['id'] == int(pk):
            current_room = room
    context = {'room': current_room}
    return render(request, 'base/room.html', context=context)
