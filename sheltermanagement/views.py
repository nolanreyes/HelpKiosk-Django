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
            return redirect('room_details', id=room.id)
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
        return redirect('room_details', id=room.id)
    if request.method == 'POST':
        form = BedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            return redirect('room_details', id=room.id)
    else:
        form = BedForm(instance=bed)
    return render(request, 'sheltermanagement/bed_form.html', {'form': form, 'room': room, 'bed': bed})


def free_up_bed(request, bed_id):
    bed = get_object_or_404(Bed, id=bed_id)
    bed.is_occupied = False
    bed.guest = None
    bed.save()
    messages.success(request, f"Bed {bed.bed_number} has been freed up successfully.")
    return redirect('room_details', id=bed.room.id)


def guests(request):
    guests = Guest.objects.all().select_related('bed__room').order_by('bed__room__room_number')
    return render(request, 'sheltermanagement/guests.html', {'guests': guests})


def allocate_bed_to_guest(request, wallet_address):
    # Assuming your function returns True if allocation is successful, otherwise False
    if allocate_bed_to_guest_by_wallet(wallet_address):
        messages.success(request, "Bed allocated successfully.")
    else:
        messages.error(request, "Allocation failed. No matching bed or guest not found.")
    return redirect('guests')


def allocate_bed_to_guest_by_wallet(wallet_address):
    from .models import Guest, Bed, Room
    try:
        guest = Guest.objects.get(wallet_address=wallet_address)
        # Find beds in rooms that match the guest's gender or are mixed (X),
        # and are not currently occupied by another guest.
        available_beds = Bed.objects.filter(
            room__gender_allocation__in=[guest.gender, 'X'],
            is_occupied=False
        ).select_related('room').order_by('room__room_number')

        if available_beds.exists():
            bed_to_allocate = available_beds.first()
            bed_to_allocate.guest = guest
            bed_to_allocate.is_occupied = True
            bed_to_allocate.save()
            print(f"Allocated bed in room {bed_to_allocate.room.room_number} to guest with wallet {wallet_address}.")
            return True
        else:
            print("No available beds match the guest's gender.")
            return False
    except Guest.DoesNotExist:
        print("Guest with wallet address not found.")
        return False


def management(request):
    # Logic for management/operations
    return render(request, 'sheltermanagement/management.html')
