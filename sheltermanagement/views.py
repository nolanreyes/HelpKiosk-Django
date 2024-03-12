from django.shortcuts import render, get_object_or_404
from sheltermanagement.models import Room


def base(request):
    # Logic for dashboard
    return render(request, 'sheltermanagement/base.html')


def dashboard(request):
    # Logic for dashboard
    return render(request, 'sheltermanagement/dashboard.html')


def rooms_display(request):
    rooms = Room.objects.all()
    return render(request, 'sheltermanagement/rooms.html', {'rooms': rooms})


def room_details(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'sheltermanagement/room_details.html', {'room': room})


def beds(request):
    # Logic for beds
    return render(request, 'sheltermanagement/beds.html')


def guests(request):
    # Logic for guests
    return render(request, 'sheltermanagement/guests.html')


def management(request):
    # Logic for management/operations
    return render(request, 'sheltermanagement/management.html')
