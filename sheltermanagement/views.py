from django.shortcuts import render

from sheltermanagement.models import Room


def base(request):
    # Logic for dashboard
    return render(request, 'sheltermanagement/base.html')


def dashboard(request):
    # Logic for dashboard
    return render(request, 'sheltermanagement/dashboard.html')


def rooms(request):
    # Fetch rooms data
    rooms = Room.objects.all()
    return render(request, 'sheltermanagement/rooms.html', {'rooms': rooms})


def beds(request):
    # Logic for beds
    return render(request, 'sheltermanagement/beds.html')


def guests(request):
    # Logic for guests
    return render(request, 'sheltermanagement/guests.html')


def management(request):
    # Logic for management/operations
    return render(request, 'sheltermanagement/management.html')
