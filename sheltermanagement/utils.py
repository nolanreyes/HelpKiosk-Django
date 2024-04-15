from django.db.models import Q, Count
from .models import Room, Bed, Booking
from django.utils import timezone


def handle_new_booking_event(booking_data):
    rooms = Room.objects.annotate(
        available_beds_count=Count('beds', filter=Q(beds__is_occupied=False))
    ).filter(
        Q(gender_allocation=booking_data['gender']) | Q(gender_allocation=Room.Gender.NONE),
        available_beds_count__gt=0
    ).order_by('available_beds_count')

    for room in rooms:
        available_bed = room.beds.filter(is_occupied=False).first()
        if available_bed:
            Booking.objects.create(
                bed=available_bed,
                check_in_date=booking_data['check_in_date'],
                check_out_date=booking_data['check_out_date']
            )

            available_bed.is_occupied = True
            available_bed.save()

            # Check if all beds in the room are now occupied to update the room to full
            if not room.beds.filter(is_occupied=False).exists():
                room.is_full = True
                room.save()

            return True, "Booking successful."

    return False, "No available rooms match the criteria."
