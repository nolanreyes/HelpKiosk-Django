from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Room, Bed, Guest
from .forms import BedForm


def base(request):
    # base
    return render(request, 'sheltermanagement/base.html')


def dashboard(request):
    # dashboard
    return render(request, 'sheltermanagement/dashboard.html')


def rooms_display(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'sheltermanagement/rooms.html', {'rooms': rooms})


def room_details(request, id):
    room = get_object_or_404(Room, id=id)
    beds = room.beds.all().order_by('bed_number')
    return render(request, 'sheltermanagement/room_details.html', {'room': room, 'beds': beds})


def add_bed(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    bed = Bed(room=room)
    if request.method == 'POST':
        form = BedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            room.capacity += 1
            room.save()
            return redirect('shelter_room_details', id=room.id)
    else:
        form = BedForm(instance=bed)
        return render(request, 'sheltermanagement/bed_form.html', {'form': form, 'room': room, 'bed': bed})


def edit_bed(request, room_id, bed_id):
    room = get_object_or_404(Room, id=room_id)
    bed = get_object_or_404(Bed, id=bed_id)
    if 'delete' in request.POST:
        bed.delete()
        room.capacity -= 1
        room.save()
        return redirect('shelter_room_details', id=room.id)
    if request.method == 'POST':
        form = BedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            return redirect('shelter_room_details', id=room.id)
    else:
        form = BedForm(instance=bed)
    return render(request, 'sheltermanagement/bed_form.html', {'form': form, 'room': room, 'bed': bed})


def free_up_bed(request, bed_id):
    # fetch the bed from the database
    bed = get_object_or_404(Bed, id=bed_id)
    # set the bed as not occupied and remove the guest from the bed
    bed.is_occupied = False
    bed.guest = None
    bed.save()
    messages.success(request, f"bed {bed.bed_number} has been freed up successfully")
    return redirect('shelter_room_details', id=bed.room.id)


def guests(request):
    guests = Guest.objects.all().select_related('bed__room').order_by('bed__room__room_number')
    return render(request, 'sheltermanagement/guests.html', {'guests': guests})


def allocate_bed_to_guest(request, wallet_address):
    try:
        # fetch the guest from the database using the wallet address
        guest = Guest.objects.get(wallet_address=wallet_address)
        # find the first available bed that matches the guest gender
        bed_to_allocate = Bed.objects.filter(
            room__gender_allocation__in=[guest.gender, 'X'],
            is_occupied=False
        ).order_by('room__room_number').first()
        # allocate bed and mark as occupied
        if bed_to_allocate:
            bed_to_allocate.guest = guest
            bed_to_allocate.is_occupied = True
            bed_to_allocate.save()
            print(f"Allocated bed in room {bed_to_allocate.room.room_number} to guest with wallet {wallet_address}.")
            messages.success(request, "Bed allocated successfully.")
        else:
            # no available bed return statement
            print("No available beds match the guest's gender.")
            messages.error(request, "Allocation failed. No matching bed or guest not found.")
    except Guest.DoesNotExist:
        # If the guest is not found, log the failure and notify the user.
        print("Guest with wallet address not found.")
        messages.error(request, "Allocation failed. No matching bed or guest not found.")
    return redirect('shelter_guests')


def management(request):
    # code for management
    return render(request, 'sheltermanagement/management.html')
